from django.shortcuts import render, HttpResponseRedirect
from django.template import RequestContext

from netrunner.apps.league.models import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

#from netrunner.apps.league.views import player_page_data

from datetime import datetime

def league_registration(request, player=None):
    now = datetime.now()
    leagues = MeetupLeague.objects.filter(start_date__gte=now).order_by('start_date')
    if len(leagues) > 0:
        current_league = leagues[0]
    else:
        current_league = None

    registered = False
    players = LeaguePlayer.objects.filter(league=current_league,player=player)
    if len(players) > 0:
        registered = True
    return current_league, registered
