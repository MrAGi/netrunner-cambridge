from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

import datetime

#class Player(models.Model):
#    player = models.OneToOneField(User)

class FactionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Faction(models.Model):
    name = models.CharField(max_length=100)
    faction_type = models.ForeignKey(FactionType,related_name='faction_type',db_index=True)

    def __str__(self):
        return self.name

class Identity(models.Model):
    class Meta:
        verbose_name_plural = "identities"
    name = models.CharField(max_length=100)
    faction = models.ForeignKey(Faction,related_name="faction",db_index=True)

    def __str__(self):
        return self.name

    def value_name(self):
        return self.name.lower().replace(" ","-")

class WinType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MeetupLeague(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    registration_start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    registration_end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    elo_starting_points = models.IntegerField(default=1500)

    def __str__(self):
        return "{0} - starting: {1}".format(self.name,self.start_date)


class Match(models.Model):
    class Meta:
        verbose_name_plural = "matches"

    date = models.DateTimeField(auto_now=False,auto_now_add=False)
    player_one = models.ForeignKey(User, related_name="player_one",db_index=True)
    player_two = models.ForeignKey(User, related_name="player_two",db_index=True)
    league = models.ForeignKey(MeetupLeague, related_name="match_league", db_index=True)

    def __str__(self):
        return "({0}) - {1} (P1) vs. {2} (P2)".format(self.date, self.player_one, self.player_two)

class GameResult(models.Model):
    player_one_agenda_points = models.PositiveIntegerField(validators=[MaxValueValidator(7),MinValueValidator(0)])
    player_two_agenda_points = models.PositiveIntegerField(validators=[MaxValueValidator(7),MinValueValidator(0)])
    player_one_identity = models.ForeignKey(Identity, related_name="identity", db_index=True, null=True)
    player_two_identity = models.ForeignKey(Identity, related_name="identity2", db_index=True, null=True)
    win_type = models.ForeignKey(WinType, related_name='win_type', db_index=True)
    pair = models.ForeignKey(Match,related_name="match", db_index=True)
    validated = models.BooleanField()

    def __str__(self):
        return "{7}: {1} ({0}) vs. {3} ({2}) - {4} ({5}-{6})".format(self.player_one_identity, self.pair.player_one,self.player_two_identity,self.pair.player_two,self.win_type,self.player_one_agenda_points,self.player_two_agenda_points,self.pair.date)


class LeaguePlayer(models.Model):
    class Meta:
        unique_together = ('league', 'player')

    league = models.ForeignKey(MeetupLeague, related_name="league", db_index=True)
    player = models.ForeignKey(User, related_name="player", db_index=True)

    def __str__(self):
        return "{0} - ({1} {2})".format(self.league.name,self.player.first_name,self.player.last_name)

class LeagueStatus(models.Model):
    class Meta:
        verbose_name_plural = "league statuses"
        unique_together = ('league', 'player','date')

    player = models.ForeignKey(LeaguePlayer, related_name="player_status", db_index=True)
    date = models.DateTimeField(auto_now=False,auto_now_add=False)
    league = models.ForeignKey(MeetupLeague, related_name="status_league", db_index=True)
    overall_elo_points = models.IntegerField()
    corp_elo_points = models.IntegerField()
    runner_elo_points = models.IntegerField()
    overall_start_elo_rank = models.IntegerField()
    corp_start_elo_rank = models.IntegerField()
    runner_start_elo_rank = models.IntegerField()
    corp_wins = models.IntegerField()
    runner_wins = models.IntegerField()
    corp_loses = models.IntegerField()
    runner_loses = models.IntegerField()
    flatline_wins = models.IntegerField()
    corp_timed_wins = models.IntegerField()
    mill_wins = models.IntegerField()
    runner_timed_wins = models.IntegerField()
    unique_opponents = models.ManyToManyField(LeaguePlayer, related_name="unique_opponents", db_index= True)

    def __str__(self):
        return "{0} - ({1} {2})".format(self.player,self.date,self.league)


class Subscriptions(models.Model):

    player = models.ForeignKey(User, related_name="subscribed_player", db_index=True)
    subscribed = models.BooleanField(default=False)
