from django.shortcuts import render, HttpResponseRedirect
from django.template import RequestContext

from netrunner.apps.league.models import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

K_FACTOR_LOW = 16
K_FACTOR_MEDIUM = 24
K_FACTOR_HIGH = 32


def calculate_k_factor(board_starting_rating, competitor_rating):
    # game importance
    k_factor = 0
    if competitor_rating >= (board_starting_rating * 1.5):
        k_factor = K_FACTOR_LOW
    elif competitor_rating >= (board_starting_rating * 1.3125):
        k_factor = K_FACTOR_MEDIUM
    else:
        k_factor = K_FACTOR_HIGH
    return k_factor

def generate_elo_points(board_starting_rating, winner_rating, loser_rating):
    winner_k = calculate_k_factor(board_starting_rating, winner_rating)
    loser_k = calculate_k_factor(board_starting_rating, loser_rating)

    rating_disparity = 400

    expected_winner_score = 1 / (1 + 10 ** ((loser_rating - winner_rating)/rating_disparity))
    expected_loser_score = 1 / (1 + 10 ** ((winner_rating - loser_rating)/rating_disparity))
    print(expected_winner_score)

    winner_delta = round(winner_k * (1 - expected_winner_score), 0)
    loser_delta = round(loser_k * (0 - expected_loser_score), 0)

    return winner_delta, loser_delta


def create_player_status(player, player_statuses, current_league, current_date):
    # player has either hasn't played or hasn't played today
    if len(player_statuses) == 0:
        # hasn't played in league yet
        corp_elo = current_league.elo_starting_points
        runner_elo = current_league.elo_starting_points
        unique_opponents = []
        corp_wins = 0
        runner_wins = 0
        corp_loses = 0
        runner_loses = 0
        flatline_wins = 0
        corp_timed_wins = 0
        mill_wins = 0
        runner_timed_wins = 0

    else:
        corp_elo = player_statuses[0].corp_start_elo_rank + player_statuses[0].corp_elo_points
        runner_elo = player_statuses[0].runner_start_elo_rank + player_statuses[0].runner_elo_points
        unique_opponents = player_statuses[0].unique_opponents.all()
        corp_wins = player_statuses[0].corp_wins
        runner_wins = player_statuses[0].runner_wins
        corp_loses = player_statuses[0].corp_loses
        runner_loses =player_statuses[0].runner_loses
        flatline_wins = player_statuses[0].flatline_wins
        corp_timed_wins = player_statuses[0].corp_timed_wins
        mill_wins = player_statuses[0].mill_wins
        runner_timed_wins = player_statuses[0].runner_timed_wins

    #create a status for this week
    new_status = LeagueStatus(player=player,
                            date=current_date,
                            league=current_league,
                            overall_elo_points=0,
                            corp_elo_points=0,
                            runner_elo_points=0,
                            overall_start_elo_rank=int((corp_elo + runner_elo) / 2),
                            corp_start_elo_rank=corp_elo,
                            runner_start_elo_rank=runner_elo,
                            corp_wins=corp_wins,
                            runner_wins=runner_wins,
                            corp_loses=corp_loses,
                            runner_loses=runner_loses,
                            flatline_wins=flatline_wins,
                            corp_timed_wins=corp_timed_wins,
                            mill_wins=mill_wins,
                            runner_timed_wins=runner_timed_wins)

    new_status.save()
    if len(unique_opponents) > 0:
        new_status.unique_opponents = unique_opponents

    return new_status


def update_league_status(game1, game2):
    current_league = game1.pair.league
    current_date = game1.pair.date
    # get league status for each player for the current league
    player_one = LeaguePlayer.objects.get(player=game1.pair.player_one,league=current_league)
    player_two = LeaguePlayer.objects.get(player=game1.pair.player_two,league=current_league)

    player1_statuses = LeagueStatus.objects.filter(player=player_one, league=current_league).order_by("-date")
    player2_statuses = LeagueStatus.objects.filter(player=player_two, league=current_league).order_by("-date")


    if len(player1_statuses) == 0 or (current_date - player1_statuses[0].date) > datetime.timedelta(days = 1):
        player1_status = create_player_status(player_one, player1_statuses, current_league, current_date)
    else:
        player1_status = player1_statuses[0]


    if len(player2_statuses) == 0 or (current_date - player2_statuses[0].date) > datetime.timedelta(days = 1):
        player2_status = create_player_status(player_two, player2_statuses, current_league, current_date)
    else:
        player2_status = player2_statuses[0]

    # get the points for each game
    corp_win_types = WinType.objects.filter(name__icontains="Corp")
    runner_win_types = WinType.objects.filter(name__icontains="Runner")

    # game 1
    if game1.win_type in corp_win_types:
        # player 1 won this game as corp
        p1_g1_points, p2_g1_points = generate_elo_points(current_league.elo_starting_points, player1_status.corp_start_elo_rank, player2_status.runner_start_elo_rank)
        player1_status.corp_wins += 1
        player2_status.runner_loses += 1
        if game1.win_type.name == "Corp Flatline":
            player1_status.flatline_wins += 1
        elif game1.win_type.name == "Corp Timed":
            player1_status.corp_timed_wins += 1
    else:
        # player 2 won this game as runner
        p2_g1_points, p1_g1_points = generate_elo_points(current_league.elo_starting_points, player2_status.runner_start_elo_rank, player1_status.corp_start_elo_rank)
        player2_status.runner_wins += 1
        player1_status.corp_loses += 1
        if game1.win_type.name == "Runner Mill":
            player2_status.mill_wins += 1
        elif game1.win_type == "Runner Timed":
            player2_status.runner_timed_wins += 1

    # game 2
    if game2.win_type in runner_win_types:
        # player 1 won this game as runner
        p1_g2_points, p2_g2_points = generate_elo_points(current_league.elo_starting_points, player1_status.runner_start_elo_rank, player2_status.corp_start_elo_rank)
        player1_status.runner_wins += 1
        player2_status.corp_loses += 1
        if game2.win_type.name == "Runner Mill":
            player1_status.mill_wins += 1
        elif game2.win_type.name == "Runner Timed":
            player1_status.runner_timed_wins += 1
    else:
        # player 2 won this game as corp
        p2_g2_points, p1_g2_points = generate_elo_points(current_league.elo_starting_points, player2_status.corp_start_elo_rank, player1_status.runner_start_elo_rank)
        player2_status.corp_wins += 1
        player1_status.runner_loses += 1
        if game2.win_type == "Corp Flatline":
            player2_status.flatline_wins += 1
        elif game2.win_type == "Corp Timed":
            player2_status.corp_timed_wins += 1

    # check for timed wins
    if "Timed" in game1.win_type.name:
        p1_g1_points = p1_g1_points / 2
        p2_g1_points = p2_g1_points / 2

    if "Timed" in game2.win_type.name:
        p1_g2_points = p1_g2_points / 2
        p2_g2_points = p2_g2_points / 2

    # update points
    player1_status.corp_elo_points += p1_g1_points
    player1_status.runner_elo_points += p1_g2_points

    player2_status.corp_elo_points += p2_g2_points
    player2_status.runner_elo_points += p2_g1_points

    #add unique opponents
    if player_two not in player1_status.unique_opponents.all():
        player1_status.unique_opponents.add(player_two)

    if player_one not in player2_status.unique_opponents.all():
        player2_status.unique_opponents.add(player_one)

    # save results
    player1_status.save()
    player2_status.save()

def elo_league_data():
    now = datetime.datetime.now()
    current_league = MeetupLeague.objects.filter(start_date__lte=now,end_date__gte=now).order_by("start_date")
    if len(current_league) > 0:
        current_league = current_league[0]
        league_players = LeaguePlayer.objects.filter(league=current_league)

        league_statuses = []
        for player in league_players:
            latest_status = LeagueStatus.objects.filter(player=player).order_by("-date")[:1]
            if latest_status:
                league_statuses.append(latest_status[0])

        #5th sort by last name
        league_statuses.sort(key = lambda x: x.player.player.first_name)
        #4th sort by last name
        league_statuses.sort(key = lambda x: x.player.player.last_name)
        #3rd sort by unique opponents
        league_statuses.sort(key = lambda x: len(x.unique_opponents.all()))
        #secondary sort by games played
        league_statuses.sort(key = lambda x: (x.corp_wins + x.corp_loses + x.runner_wins + x.runner_loses))
        #primary sort by overall elo points
        league_statuses.sort(key = lambda x: (x.corp_elo_points + x.runner_elo_points + x.corp_start_elo_rank + x.runner_start_elo_rank)//2, reverse=True)
    else:
        league_statuses = []
    return league_statuses

