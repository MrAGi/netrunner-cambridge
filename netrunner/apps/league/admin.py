from django.contrib import admin

from netrunner.apps.league.models import *

# Register your models here.
#admin.site.register(Player)
admin.site.register(FactionType)
admin.site.register(Faction)
admin.site.register(Identity)
admin.site.register(WinType)
admin.site.register(GameResult)
admin.site.register(Match)
admin.site.register(MeetupLeague)
admin.site.register(LeaguePlayer)
admin.site.register(LeagueStatus)
admin.site.register(Subscriptions)