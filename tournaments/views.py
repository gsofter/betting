from django.shortcuts import render
from django.http import HttpResponse

from .models import ATPTournament
from .models import WTATournament
from modules import tournamentscrapping

# Create your views here.
def atp_tournament_list(request):
    tournaments = tournamentscrapping.get_atp_tournaments()
    context = {
        'tournaments' : tournaments
    }

    return render(request, 'tournament/tournament_list.html', context)
    
def wta_tournament_list(request):
    tournaments = tournamentscrapping.get_wta_tournaments()
    context = {
        'tournaments' : tournaments
    }

    return render(request, 'tournament/tournament_list.html', context)
    