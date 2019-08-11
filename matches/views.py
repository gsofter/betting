from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import matchSerializer
from .models import Match, ATPMatch
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
    for match in matches:
        try:
            old_matches = ATPPlayer.objects.filter(home = match['home'], 
                                                    away = match['away'], 
                                                    date = match['date'])
            #Check whether it exists or not in database
            if len(old_matches) > 0:
                old_m = old_matches[0]
                old_m.round = match['round']
                old_m.winner = match['winner']
                old_m.loser = match['loser']
                old_m.status = match['status']
                old_m.comment = match['comment']
                old_m.w1 = match['w1']
                old_m.l1 = match['l1']
                old_m.w2 = match['w2']
                old_m.l2 = match['l2']
                old_m.w3 = match['w3']
                old_m.l3 = match['l3']
                old_m.w4 = match['w4']
                old_m.l4 = match['l4']
                old_m.w5 = match['w5']
                old_m.l5 = match['l5']
                old_m.wsets = match['wsets']
                old_m.lsets = match['lsets']
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
        new_m.w1 = match['w1']
        new_m.l1 = match['l1']
        new_m.w2 = match['w2']
        new_m.l2 = match['l2']
        new_m.w3 = match['w3']
        new_m.l3 = match['l3']
        new_m.w4 = match['w4']
        new_m.l4 = match['l4']
        new_m.w5 = match['w5']
        new_m.l5 = match['l5']
        new_m.wsets = match['wsets']
        new_m.lsets = match['lsets']
        new_m.totalsets = match['totalsets']
        new_m.totalgames = match['totalgames']
        new_m.bestof = match['bestof']
        new_m.save()
    return HttpResponse("<h1> Update ATP Match function called!!! </h1>")

def remove_atp_match(request):
    ATPMatch.objects.all().delete()
    return HttpResponse("<h1> Success </h1>")

def update_atp_perform(request):
    results = matchscrapping.get_atp_match_from_flashresultat()
    for performdata in results:
        try:
            old_matches = ATPMatch.objects.all().filter(home = performdata['home'],away = performdata['away'])
            #Check whether it exists or not in database
            if len(old_matches) > 0:
                old_m = old_matches[0]
                old_m.waces = performdata['waces']
                old_m.wdfault = performdata['wdfault']
                old_m.wser1 = performdata['wser1']
                old_m.wser2 = performdata['wser2']
                old_m.wser = performdata['wser']
                old_m.wrec = performdata['wrec']
                old_m.wtotal = performdata['wtotal']
                old_m.laces = performdata['laces']
                old_m.ldfault = performdata['ldfault']
                old_m.lser1 = performdata['lser1']
                old_m.lser2 = performdata['lser2']
                old_m.lser = performdata['lser']
                old_m.lrec = performdata['lrec']
                old_m.ltotal = performdata['ltotal']
                old_m.save()
                continue
        except:
            print(performdata['home'])
    return HttpResponse("<h1> Success </h1>")