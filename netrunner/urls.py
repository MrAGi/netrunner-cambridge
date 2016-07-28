from django.conf.urls import patterns, include, url
from django.contrib import admin
from netrunner.apps.league.views import league_status, home_page, player_page, logout_page, report_form, process_report, validate_games, register_for_league, subscribe, unsubscribe
from netrunner.apps.discourse import views
from .settings import STATIC_ROOT
from django.views.generic.base import TemplateView


urlpatterns = patterns('',
        url(r'^accounts/', include('registration.backends.default.urls')),
        url(r'^admin/', include(admin.site.urls)),
        url(r'^league/', league_status),
        url(r'^$', home_page),
        url(r'accounts/profile/', player_page),
        url(r'^players/(?P<first>[a-z]*)\-(?P<last>[a-z\-]*)/$', player_page),
        url(r'^registerforleague/',register_for_league),
        url(r'^login/$', 'django.contrib.auth.views.login'),
        url(r'^logout/$', logout_page),
        url(r'^report/$', report_form),
        url(r'^processreport/$',process_report),
        url(r'^validategames/$',validate_games),
        url(r'^discourse/sso$', views.sso),
        url(r'^success/$',subscribe),
        url(r'^cancel/$',unsubscribe),
)