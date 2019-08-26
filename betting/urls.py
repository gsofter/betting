"""betting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

from .views import homepage
from players.views import player_index
from matches.views import *
from tournaments.views import atp_tournament_list,  wta_tournament_list

urlpatterns = [
    #admin paths
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('admin/', admin.site.urls),

    path('', homepage, name="home"),
    path('player/',include('players.urls', namespace='player')),

    #match pathes   
    path('match/atp', atp_match_list, name="atp_match_list"),
    path('match/wta', wta_match_list, name="wta_match_list"),

    #odds math
    path('match/odd_atp', atp_odd_list, name="atp_odds_list"),
    path('match/odd_wta', wta_odd_list, name="wta_odds_list"),
    
    #tournaments pathes
    path('tour/atp/', atp_tournament_list, name="atp_tour_list"),
    path('tour/wta/', wta_tournament_list, name="wta_tour_list"),

    #http requests
    path('match/update_atp_match/', update_atp_match, name='update_atp_match'),
    path('match/remove_atp_match/', remove_atp_match, name='remove_atp_match'),
    path('match/update_atp_perform/', update_atp_perform, name='update_atp_perform'),
    path('match/import_atp', import_atp_match, name="import_atp_match"),
    path('match/import_wta', import_wta_match, name="import_wta_match"),
    #jet admin urls
    path('jet_api/', include('jet_django.urls')),

    #functions
    path('change/', change_winna_to_max, name="change_winna_to_max"),
]
