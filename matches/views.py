from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import matchSerializer
from .models import Match, ATPMatch
from players.models import ATPPlayer, WTAPlayer
from modules import matchscrapping, oddscraping

class matchList(APIView):
    def get(self, arges):
        matches = Match.objects.all()[:25]
        serializer = matchSerializer(matches, many=True)
        return Response(serializer.data)
        
    def post(self):
        pass

def match_list(request):
    match_list = Match.objects.all()
    paginator = Paginator(match_list, 10)
    page = request.GET.get('page', 1)
    matches = paginator.get_page(page)

    items_cnt = 0
    if page == 1:
        items_cnt = 0
    else:
        items_cnt = int(page,10) * 10
    
    context = {
        'matches' : matches,
        'items_cnt' : items_cnt, 
        'page_number' : page, 
    }    
    return render(request, 'match/match_list.html', context)

def atp_match_list(request):
    #match_list = matchscrapping.get_atp_matches_from_xscores()
    match_list = ATPMatch.objects.all()[:100]
    context = {
        'matches' : match_list,
    }
    return render(request, 'match/match_list1.html', context)

def wta_match_list(request):
    match_list = matchscrapping.get_atp_matches_from_xscores()
    context = {
        'matches' : match_list,
    }
    return render(request, 'match/match_list1.html', context)

def match_home(request):
    return HttpResponse("<h1> Welcome matches </h1>")

def atp_odd_list(request):
    odds_data = oddscraping.get_odds_data()
    data = odds_data['atpodds']
    context = {
        'odds' : data,
    }
    return render(request, template_name="match/odd_list.html", context=context)


def wta_odd_list(request):
    odds_data = oddscraping.get_odds_data()
    data = odds_data['wtaodds']
    context = {
        'odds' : data,
    }
    return render(request, template_name="match/odd_list.html", context=context)

#HTTP requests processor
def update_atp_match(request):
    matches = matchscrapping.get_atp_matches_from_xscores()
    
    #filter match player names with player database
    for match in matches:
        home = match['home'].upper()
        away = match['away'].upper()
        try:
            home_player = ATPPlayer.objects.filter(nicknames__contains=home)
            away_player = ATPPlayer.objects.filter(nicknames__contains=away)
            
            if len(home_player) > 0:
                match['home'] = home_player[0].name
            else:
                print(home)

            if len(away_player) > 0:
                match['away'] = away_player[0].name
            else:
                print(away)

        except:
            print(home)

    for match in matches:
        try:
            old_matches = ATPMatch.objects.filter(home = match['home'], 
                                                    away = match['away'])
            #Check whether it exists or not in database
            if len(old_matches) > 0:
                old_m = old_matches[0]
                old_m.round = match['round']
                old_m.winner = match['winner']
                old_m.loser = match['loser']
                old_m.status = match['status']
                old_m.comment = match['comment']
                old_m.home_r1 = match['home_r1']
                old_m.away_r1 = match['away_r1']
                old_m.home_r2 = match['home_r2']
                old_m.away_r2 = match['away_r2']
                old_m.home_r3 = match['home_r3']
                old_m.away_r3 = match['away_r3']
                old_m.home_r4 = match['home_r4']
                old_m.away_r4 = match['away_r4']
                old_m.home_r5 = match['home_r5']
                old_m.away_r5 = match['away_r5']
                old_m.home_winsets = match['home_winsets']
                old_m.away_winsets = match['away_winsets']
                old_m.totalsets = match['totalsets']
                old_m.totalgames = match['totalgames']
                old_m.bestof = match['bestof']
                old_m.save()
                continue
        except:
            print(match['home'])
        new_m = ATPMatch()
        new_m.date = match['date']
        new_m.round = match['round']
        new_m.tournament = match['tournament']
        new_m.status = match['status']
        new_m.comment = match['comment']
        new_m.home = match['home']
        new_m.away = match['away']
        new_m.winner = match['winner']
        new_m.loser = match['loser']
        new_m.home_r1 = match['home_r1']
        new_m.away_r1 = match['away_r1']
        new_m.home_r2 = match['home_r2']
        new_m.away_r2 = match['away_r2']
        new_m.home_r3 = match['home_r3']
        new_m.away_r3 = match['away_r3']
        new_m.home_r4 = match['home_r4']
        new_m.away_r4 = match['away_r4']
        new_m.home_r5 = match['home_r5']
        new_m.away_r5 = match['away_r5']
        new_m.home_winsets = match['home_winsets']
        new_m.away_winsets = match['away_winsets']
        new_m.totalsets = match['totalsets']
        new_m.totalgames = match['totalgames']
        new_m.bestof = match['bestof']
        new_m.save()
    return HttpResponse("<h1> Update ATP Match function called!!! </h1>")

def remove_atp_match(request):
    ATPMatch.objects.all().delete()
    return HttpResponse("<h1> Success </h1>")

def update_atp_perform(request):
    return HttpResponse("<h1> Success </h1>")