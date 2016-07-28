from django.shortcuts import render, HttpResponseRedirect
from django.template import RequestContext

from netrunner.apps.league.models import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from registration.views import RegistrationView
from netrunner.apps.league.league_registration import league_registration
from netrunner.apps.league.elo_league import update_league_status, elo_league_data

import datetime

def custom_proc(request):
    return {'user': request.user}

def league_data_charlie():
    users = {user: {
        'base_score': 50,
        'bonus_points': 0,
        'total_score': 0,
        'played': 0,
        'corp_win': 0,
        'corp_loss': 0,
        'runner_win': 0,
        'runner_loss': 0,
        'unique_opponents': [],
        'flatline_wins': 0,
        'mill_wins': 0
    } for user in User.objects.all()}

    corp_win_types = WinType.objects.filter(name__contains="Corp")
    runner_win_types = WinType.objects.filter(name__contains="Runner")

    flatline = WinType.objects.get(name__iexact="Corp Flatline")
    mill = WinType.objects.get(name__iexact="Runner Mill")

    corp = FactionType.objects.get(name__iexact="Corp")
    runner = FactionType.objects.get(name__iexact="Runner")

    games = GameResult.objects.all()

    for game in games:
        if game.validated == True:
            p1 = game.pair.player_one
            p2 = game.pair.player_two

            # increment games played
            users[p1]['played'] += 1
            users[p2]['played'] += 1

            p1_faction_type = game.player_one_identity.faction.faction_type
            p2_faction_type = game.player_two_identity.faction.faction_type

            # update player one wins and loses
            if p1_faction_type == corp and game.win_type in corp_win_types:
                # player one won as the corp
                # print("p1 won as the corp")
                users[p1]['corp_win'] += 1
                users[p1]['base_score'] += 2
                if game.win_type == flatline:
                    users[p1]['flatline_wins'] += 1
            elif p1_faction_type == corp and game.win_type not in corp_win_types:
                # player one lost as the corp
                # print("p1 lost as the corp")
                users[p1]['corp_loss'] += 1
                users[p1]['base_score'] -= 2
            elif p1_faction_type == runner and game.win_type in runner_win_types:
                # player one won as the runner
                # print("p1 won as the runner")
                users[p1]['runner_win'] += 1
                users[p1]['base_score'] += 2
                if game.win_type == mill:
                    users[p1]['mill_wins'] += 1
            elif p1_faction_type == runner and game.win_type not in runner_win_types:
                # player one lost as the runner
                # print("p1 lost as the runner")
                users[p1]['runner_loss'] += 1
                users[p1]['base_score'] -= 2
            else:
                # print("something went wrong")
                pass

            # update player two wins and loses
            if p2_faction_type == corp and game.win_type in corp_win_types:
                # player one won as the corp
                # print("p2 won as the corp")
                users[p2]['corp_win'] += 1
                users[p2]['base_score'] += 2
                if game.win_type == flatline:
                    users[p2]['flatline_wins'] += 1
            elif p2_faction_type == corp and game.win_type not in corp_win_types:
                # player one lost as the corp
                # print("p2 lost as the corp")
                users[p2]['corp_loss'] += 1
                users[p2]['base_score'] -= 2
            elif p2_faction_type == runner and game.win_type in runner_win_types:
                # player one won as the runner
                # print("p2 won as the runner")
                users[p2]['runner_win'] += 1
                users[p2]['base_score'] += 2
                if game.win_type == mill:
                    users[p2]['mill_wins'] += 1
            elif p2_faction_type == runner and game.win_type not in runner_win_types:
                # player one lost as the runner
                # print("p2 lost as the runner")
                users[p2]['runner_loss'] += 1
                users[p2]['base_score'] -= 2
            else:
                # print("something went wrong")
                pass

            # update opponents
            if p2 not in users[p1]['unique_opponents']:
                users[p1]['unique_opponents'].append(p2)

            if p1 not in users[p2]['unique_opponents']:
                users[p2]['unique_opponents'].append(p1)

    for user in users:
        # bonus points for winning as corp + runner

        corp_wins = users[user]['corp_win']
        runner_wins = users[user]['runner_win']

        if corp_wins == runner_wins:
            bonus = corp_wins
        elif corp_wins == 0 or runner_wins == 0:
            bonus = 0
        elif (corp_wins >= 1 and runner_wins >= 1) and corp_wins < runner_wins:
            bonus = corp_wins
        elif (corp_wins >= 1 and runner_wins >= 1) and corp_wins > runner_wins:
            bonus = runner_wins

        if bonus > 8:
            bonus = 8

        users[user]['bonus_points'] += bonus

        # bonus points for playing different opponents
        unique = len(users[user]['unique_opponents'])

        if unique > 8:
            unique = 8

        users[user]['bonus_points'] += unique

        # generate total score
        users[user]['total_score'] = users[user]['base_score'] + users[user]['bonus_points']

        users[user]['unique_opponents'] = len(users[user]['unique_opponents'])

    # convert to list
    test = list(users.items())

    # sort mill wins (5th)
    s = sorted(test, key=lambda x: x[1]['mill_wins'], reverse=True)
    # sort flatline wins (4th)
    s = sorted(test, key=lambda x: x[1]['flatline_wins'], reverse=True)
    # sort by bonus points (3th)
    s = sorted(s, key=lambda x: x[1]['bonus_points'], reverse=True)
    # sort by base score (2nd)
    s = sorted(s, key=lambda x: x[1]['base_score'], reverse=True)
    # sort by total score (1st)
    s = sorted(s, key=lambda x: x[1]['total_score'], reverse=True)

    return s


def player_game_data():
    players = User.objects.all()
    data = {}
    for player in players:
        corp = FactionType.objects.get(name__iexact="Corp")
        corp_games = game_data(player, corp)
        runner = FactionType.objects.get(name__iexact="Runner")
        runner_games = game_data(player, runner)
        data[player] = {'corp': corp_games, 'runner': runner_games}
    return data


def league_data():
    users = {user: {
        'played': 0,
        'corp_win': 0,
        'corp_loss': 0,
        'runner_win': 0,
        'runner_loss': 0,
        'agendas_for': 0,
        'agendas_against': 0,
        'agenda_difference': 0,
        'points': 0
        } for user in User.objects.all()}

    corp_win_types = WinType.objects.filter(name__contains="Corp")
    runner_win_types = WinType.objects.filter(name__contains="Runner")

    corp = FactionType.objects.get(name__iexact="Corp")
    runner = FactionType.objects.get(name__iexact="Runner")

    games = GameResult.objects.all()

    for game in games:
        p1 = game.pair.player_one
        p2 = game.pair.player_two

        # increment games played
        users[p1]['played'] += 1
        users[p2]['played'] += 1

        # increate agenda points for and against
        users[p1]['agendas_for'] += game.player_one_agenda_points
        users[p2]['agendas_for'] += game.player_two_agenda_points
        users[p1]['agendas_against'] += game.player_two_agenda_points
        users[p2]['agendas_against'] += game.player_one_agenda_points

        # update the agenda difference
        users[p1]['agenda_difference'] = users[p1]['agendas_for'] - users[p1]['agendas_against']
        users[p2]['agenda_difference'] = users[p2]['agendas_for'] - users[p2]['agendas_against']

        p1_faction_type = game.player_one_identity.faction.faction_type
        p2_faction_type = game.player_two_identity.faction.faction_type

        # update player one wins and loses

        if p1_faction_type == corp and game.win_type in corp_win_types:
            # player one won as the corp
            # print("p1 won as the corp")
            users[p1]['corp_win'] += 1
            users[p1]['points'] += 2
        elif p1_faction_type == corp and game.win_type not in corp_win_types:
            # player one lost as the corp
            # print("p1 lost as the corp")
            users[p1]['corp_loss'] += 1
        elif p1_faction_type == runner and game.win_type in runner_win_types:
            # player one won as the runner
            # print("p1 won as the runner")
            users[p1]['runner_win'] += 1
            users[p1]['points'] += 2
        elif p1_faction_type == runner and game.win_type not in runner_win_types:
            # player one lost as the runner
            # print("p1 lost as the runner")
            users[p1]['runner_loss'] += 1
        else:
            # print("something went wrong")
            pass

        # update player two wins and loses
        if p2_faction_type == corp and game.win_type in corp_win_types:
            # player one won as the corp
            # print("p2 won as the corp")
            users[p2]['corp_win'] += 1
            users[p2]['points'] += 2
        elif p2_faction_type == corp and game.win_type not in corp_win_types:
            # player one lost as the corp
            # print("p2 lost as the corp")
            users[p2]['corp_loss'] += 1
        elif p2_faction_type == runner and game.win_type in runner_win_types:
            # player one won as the runner
            # print("p2 won as the runner")
            users[p2]['runner_win'] += 1
            users[p2]['points'] += 2
        elif p2_faction_type == runner and game.win_type not in runner_win_types:
            # player one lost as the runner
            # print("p2 lost as the runner")
            users[p2]['runner_loss'] += 1
        else:
            # print("something went wrong")
            pass

    # convert to list
    test = list(users.items())

    # sort agendas against (4th)
    s = sorted(test, key=lambda x: x[1]['agendas_against'], reverse=True)
    # sort by agendas for (3th)
    s = sorted(s, key=lambda x: x[1]['agendas_for'], reverse=True)
    # sort by agenda difference (2nd)
    s = sorted(s, key=lambda x: x[1]['agenda_difference'], reverse=True)
    # sort by points (1st)
    s = sorted(s, key=lambda x: x[1]['points'], reverse=True)

    return s


def game_data(player,faction):
    #games as either player 1 or player 2)
    p1_games = GameResult.objects.filter(pair__player_one = player)
    p2_games = GameResult.objects.filter(pair__player_two = player)


    p1_games = [game for game in p1_games if (game.player_one_identity.faction.faction_type == faction and game.pair.player_one == player)]
    p2_games = [game for game in p2_games if (game.player_two_identity.faction.faction_type == faction and game.pair.player_two == player)]

    results = []
    for game in p1_games:
        data = {}
        data['date'] = game.pair.date
        data['identity'] = game.player_one_identity
        data['opponent'] = game.pair.player_two
        data['opponent_identity'] = game.player_two_identity
        data['result'] = game.win_type

        results.append(data)

    for game in p2_games:
        data = {}
        data['date'] = game.pair.date
        data['identity'] = game.player_two_identity
        data['opponent'] = game.pair.player_one
        data['opponent_identity'] = game.player_one_identity
        data['result'] = game.win_type

        results.append(data)

    return results


def unvalidated_data(games):
    results = []
    for game in games:
        data = {}
        data['date'] = game.pair.date
        data['identity'] = game.player_two_identity
        data['opponent'] = game.pair.player_one
        data['opponent_identity'] = game.player_one_identity
        data['result'] = game.win_type
        data['validated'] = game.validated
        data['id'] = game.id

        results.append(data)

    return results


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def favourite_faction(games):
    identities_used = []
    for game in games:
        identities_used.append(game["identity"])
    if len(identities_used) > 0:
        favourite_used = max(set(identities_used), key=identities_used.count)
    else:
        favourite_used = None
    return favourite_used



def league_status(request):
    league = elo_league_data()
    return render(request, 'league.html', {'league': league})


def home_page(request):
    d = datetime.datetime.now()
    mon = next_weekday(d, 0)
    return render(request, 'home.html', {'meetup': mon}, context_instance=RequestContext(request, processors=[custom_proc]))


def player_page_data(request, first=None, last=None):
    if first and last:
        player = User.objects.get(first_name__iexact=first, last_name__iexact=last)
    else :
        player = request.user
    league = elo_league_data()
    player_data = [data for data in league if data.player.player == player]
    if len(player_data) > 0:
        player_data = player_data[0]
        position = league.index(player_data) + 1
    else:
        player_data = None
        position = None
    players = len(league)
    corp = FactionType.objects.get(name__iexact="Corp")
    corp_games = game_data(player, corp)
    fav_corp = favourite_faction(corp_games)
    runner = FactionType.objects.get(name__iexact="Runner")
    runner_games = game_data(player, runner)
    fav_runner = favourite_faction(runner_games)
    #get unvalidated games
    if request.user.is_authenticated():
        unvalidated = GameResult.objects.filter(pair__player_two=player,validated=False)
        unvalidated = unvalidated_data(unvalidated)
    else:
        unvalidated = []

    #get current league registration status
    new_league, registered = league_registration(request,player)

    return player, corp_games, runner_games, player_data, position, players, fav_corp, fav_runner, unvalidated, new_league, registered


def player_page(request, first=None, last=None):
    player, corp_games, runner_games, player_data, position, players, fav_corp, fav_runner, unvalidated, new_league, registered = player_page_data(request, first, last)
    subscription_status = Subscriptions.objects.filter(player=player)
    if len(subscription_status) > 0:
        subscribed = subscription_status[0].subscribed
    else:
        subscribed = False
    return render(request, 'player.html', {'player': player, 'corp': corp_games, 'runner': runner_games,'league': player_data, 'position': position, 'players': players, 'fav_corp': fav_corp, 'fav_runner': fav_runner, 'unvalidated': unvalidated, 'new_league': new_league, 'registered': registered, 'subscribed': subscribed})

@login_required
def subscribe(request):
    player = request.user
    #player = User.objects.get(id=player.id)
    existing = Subscriptions.objects.filter(player=player)
    if len(existing) == 0:
        new_subscription = Subscriptions(player=player, subscribed=True)
        new_subscription.save()
    else:
        new_subscription = existing[0]
        new_subscription.subscribed = True
        new_subscription.save()
    return player_page(request)


@login_required
def unsubscribe(request):
    player = request.user
    #player = User.objects.get(id=player.id)
    existing = Subscriptions.objects.filter(player=player)
    if len(existing) > 0:
        cancelled_subscription = existing[0]
        cancelled_subscription.subscribed = False
        cancelled_subscription.save()
    return player_page(request)


@login_required
def register_for_league(request):
    status = request.POST.getlist("confirm_register")
    player_id = request.POST.get('player')
    league_id = request.POST.get('league')
    player = User.objects.get(id=player_id)
    league = MeetupLeague.objects.get(id=league_id)

    existing = LeaguePlayer.objects.filter(league=league, player=player)
    if len(existing) == 0 and status:
        new_league_player = LeaguePlayer(league=league, player=player)
        new_league_player.save()

    return render(request, 'registered_for_league.html', {'player': player,'registered': status})


def login(request):
    return render(request, 'login.html')


def login_process(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # correct password
        auth.login(request, user)
        # redireact to success page
        return HttpResponseRedirect("/")
    else:
        # show and error page
        return HttpResponseRedirect("/")


def logout_page(request):
    auth.logout(request)
    # redirect to success page
    return HttpResponseRedirect("/")


@login_required
def report_form(request):
    # get the league for the match
    d = datetime.datetime.now()
    if d.weekday() != 0:
        days_to_mon = 0 - d.weekday()
        day_interval = datetime.timedelta(days_to_mon)
        d = d + day_interval
    current_league = MeetupLeague.objects.all().filter(start_date__lte=d, end_date__gte=d).order_by('start_date')

    user_in_league = LeaguePlayer.objects.filter(player=request.user)


    if len(current_league) > 0 and len(user_in_league) > 0:
        if request.user.is_authenticated() and request.user.is_staff:
            players1 = LeaguePlayer.objects.filter(league=current_league).order_by('player__first_name', 'player__last_name')
            players2 = LeaguePlayer.objects.filter(league=current_league).order_by('player__first_name', 'player__last_name')
        else:
            players1 = LeaguePlayer.objects.filter(player__username=request.user.username, league=current_league).order_by('player__first_name', 'player__last_name')
            players2 = LeaguePlayer.objects.filter(league=current_league).exclude(player__username=request.user.username).order_by('player__first_name', 'player__last_name')
        runners = Identity.objects.filter(faction__faction_type__name__contains = "Runner").order_by('name')
        corps = Identity.objects.filter(faction__faction_type__name__contains = "Corp").order_by('name')
        win_types = WinType.objects.all().order_by('name')

        current_league = current_league[0]
        return render(request, 'report.html', {'reporting_closed': False, 'players1': players1, 'players2':players2, 'runners': runners, 'corps': corps,'wintypes': win_types, 'current_league': current_league}, context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        return render(request, 'report.html', {'reporting_closed': True}, context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
def process_report(request):
    player1 = request.POST.get('p1')
    p1_corp = request.POST.get('p1-corp')
    p1_runner = request.POST.get('p1-runner')

    player2 = request.POST.get('p2')
    p2_corp = request.POST.get('p2-corp')
    p2_runner = request.POST.get('p2-runner')

    g1 = request.POST.get('g1')
    g2 = request.POST.get('g2')

    current_league_id = request.POST.get('current-league')
    current_league = MeetupLeague.objects.get(id=current_league_id)


    # get players
    p1 = User.objects.get(username=player1)
    p2 = User.objects.get(username=player2)

    # get identities
    p1_corp_id = Identity.objects.get(name=p1_corp)
    p1_runner_id = Identity.objects.get(name=p1_runner)

    p2_corp_id = Identity.objects.get(name=p2_corp)
    p2_runner_id = Identity.objects.get(name=p2_runner)

    # get win types
    g1_win = WinType.objects.get(name=g1)
    g2_win = WinType.objects.get(name=g2)

    #get the date of the last meetup
    d = datetime.datetime.now(datetime.timezone.utc)
    if d.weekday() != 0:
        days_to_mon = 0 - d.weekday()
        day_interval = datetime.timedelta(days_to_mon)
        d = d + day_interval

    #check that it is not a duplicate report
    six_days = datetime.timedelta(6)
    d_before = d - six_days
    d_after = d + six_days
    #get all matches involving players
    p1_matches = Match.objects.all().filter(player_one=p1,player_two=p2,date__lte=d_after,date__gte=d_before)
    p2_matches = Match.objects.all().filter(player_one=p2,player_two=p1,date__lte=d_after,date__gte=d_before)

    matches = []
    for match in p1_matches:
        matches.append(match)
    for match in p2_matches:
        matches.append(match)

    possible_duplicate = False

    if len(matches) > 0:
        #possible duplicate
        possible_duplicate = True

    if request.user.is_staff:
        validated = True
    else:
        validated = True

    if p1 != p2 and not possible_duplicate:


        # create match
        match = Match(date=d, player_one=p1, player_two=p2, league=current_league)
        match.save()

        # create games

        game1 = GameResult(player_one_agenda_points=0,
            player_two_agenda_points=0,
            player_one_identity=p1_corp_id,
            player_two_identity=p2_runner_id,
            win_type=g1_win,
            pair=match,
            validated=validated)

        game2 = GameResult(player_one_agenda_points=0,
            player_two_agenda_points=0,
            player_one_identity=p1_runner_id,
            player_two_identity=p2_corp_id,
            win_type=g2_win,
            pair=match,
            validated=validated)

        game1.save()
        game2.save()

        #update league status for players
        update_league_status(game1, game2)

        return render(request, 'report_processed.html', {
            'player1': p1,
            'player2': p2,
            'p1_corp': p1_corp,
            'p2_corp': p2_corp,
            'p1_runner': p1_runner,
            'p2_runner': p2_runner,
            'g1': g1,
            'g2': g2},
            context_instance=RequestContext(request, processors=[custom_proc]))
    elif possible_duplicate:
        if request.user.is_authenticated() and request.user.is_staff:
            players1 = LeaguePlayer.objects.filter(league=current_league).order_by('player__first_name', 'player__last_name')
            players2 = LeaguePlayer.objects.filter(league=current_league).order_by('player__first_name', 'player__last_name')
        else:
            players1 = LeaguePlayer.objects.filter(player__username=request.user.username, league=current_league).order_by('player__first_name', 'player__last_name')
            players2 = LeaguePlayer.objects.filter(league=current_league).exclude(player__username=request.user.username).order_by('player__first_name', 'player__last_name')
        runners = Identity.objects.filter(faction__faction_type__name__contains = "Runner")
        corps = Identity.objects.filter(faction__faction_type__name__contains = "Corp")
        win_types = WinType.objects.all()

        return render(request, 'report.html', {
            'reporting_closed': False,
            'player1': player1,
            'player2': player2,
            'p1_corp': p1_corp,
            'p2_corp': p2_corp,
            'p1_runner': p1_runner,
            'p2_runner': p2_runner,
            'g1': g1,
            'g2': g2,
            'errors': "Possible duplicate report - please check your unvalidated games",
            'players1': players1,
            'players2': players2,
            'runners': runners,
            'corps': corps,
            'wintypes': win_types,
            'current_league': current_league},
            context_instance=RequestContext(request, processors=[custom_proc]))
    else:
        if request.user.is_authenticated() and request.user.is_staff:
            players1 = LeaguePlayer.objects.filter(league=current_league).order_by('player__first_name', 'player__last_name')
            players2 = LeaguePlayer.objects.filter(league=current_league).order_by('player__first_name', 'player__last_name')
        else:
            players1 = LeaguePlayer.objects.filter(player__username=request.user.username, league=current_league).order_by('player__first_name', 'player__last_name')
            players2 = LeaguePlayer.objects.filter(league=current_league).exclude(player__username=request.user.username).order_by('player__first_name', 'player__last_name')
        runners = Identity.objects.filter(faction__faction_type__name__contains = "Runner")
        corps = Identity.objects.filter(faction__faction_type__name__contains = "Corp")
        win_types = WinType.objects.all()

        return render(request, 'report.html', {
            'reporting_closed': False,
            'player1': player1,
            'player2': player2,
            'p1_corp': p1_corp,
            'p2_corp': p2_corp,
            'p1_runner': p1_runner,
            'p2_runner': p2_runner,
            'g1': g1,
            'g2': g2,
            'errors': "Players must be different",
            'players1': players1,
            'players2': players2,
            'runners': runners,
            'corps': corps,
            'wintypes': win_types,
            'current_league': current_league},
            context_instance=RequestContext(request, processors=[custom_proc]))


@login_required
def validate_games(request):
    games = request.POST.getlist("validated-games")
    for game in games:
        result = GameResult.objects.get(id=game)
        result.validated = True
        result.save()
    player = result.pair.player_two
    first_name = player.first_name.lower()
    last_name = player.last_name.lower()
    return render(request, 'validated_games.html', {'games':games, 'first_name': first_name, 'last_name': last_name}, context_instance=RequestContext(request, processors=[custom_proc]))