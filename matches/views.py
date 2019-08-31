from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ATPMatch, WTAMatch
from players.models import ATPPlayer, WTAPlayer
from modules import matchscrapping, oddscraping
import xlrd
import os
import datetime

def atp_match_list(request):
    #match_list = matchscrapping.get_atp_matches_from_xscores()
    match_list = ATPMatch.objects.all()[:100]
    context = {
        'matches' : match_list,
    }
    return render(request, 'match/match_list1.html', context)

def wta_match_list(request):
    match_list = ATPMatch.objects.all()[:100]
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

def load_xlsx_atp(filepath):
    # dirname = os.path.dirname(__file__)
    # filename = os.path.join(dirname, 'atp/2019.xlsx')
    book = xlrd.open_workbook(filepath)
    sheet = book.sheet_by_index(0)
    harr = []
    for c in range(1, sheet.ncols):
        harr.append(sheet.cell(0,c).value)

    b365w_id =  harr.index("B365W") + 1
    b365l_id =  harr.index("B365L") + 1
    maxw_id =  harr.index("MaxW") + 1
    maxl_id =  harr.index("MaxL") + 1
    psw_id =  harr.index("PSW") + 1
    psl_id =  harr.index("PSL") + 1
    avgw_id = harr.index("AvgW") + 1
    avgl_id = harr.index("AvgL") + 1

    for r in range(1, sheet.nrows):
        match = ATPMatch()
        match.location	= sheet.cell(r,1).value
        match.tournament	= sheet.cell(r,2).value
        _date	= sheet.cell(r,3).value
        match.date = datetime.datetime(*xlrd.xldate_as_tuple(_date, book.datemode))
        
        match.round = sheet.cell(r,7).value    
        match.bestof = int(sheet.cell(r,8).value)    
        match.winner = sheet.cell(r,9).value
        match.loser = sheet.cell(r,10).value
        match.home  = find_player(sheet.cell(r,9).value)
        match.away = find_player(sheet.cell(r,10).value)
        dup_match = find_duplicate(match.winner, match.loser, match.date)
        if dup_match is not None:
            continue

        match.court = sheet.cell(r,5).value
        match.surface = sheet.cell(r,6).value
        # match.wrank = sheet.cell(r,11).value
        # match.lrank = sheet.cell(r,12).value
        # match.wpts = sheet.cell(r,13).value
        # match.lpts = sheet.cell(r,14).value
    
        match.home_r1 = get_int_val(sheet.cell(r,15).value)
        match.away_r1 = get_int_val(sheet.cell(r,16).value)
        match.home_r2 = get_int_val(sheet.cell(r,17).value)
        match.away_r2 = get_int_val(sheet.cell(r,18).value)
        match.home_r3 = get_int_val(sheet.cell(r,19).value)
        match.away_r3 = get_int_val(sheet.cell(r,20).value)
        match.home_r4 = get_int_val(sheet.cell(r,21).value)
        match.away_r4 = get_int_val(sheet.cell(r,22).value)
        match.home_r5 = get_int_val(sheet.cell(r,23).value)
        match.away_r5 = get_int_val(sheet.cell(r,24).value)
        match.home_winsets = get_int_val(sheet.cell(r,25).value)
        match.away_winsets = get_int_val(sheet.cell(r,26).value)
        match.status = sheet.cell(r,27).value
        if b365w_id != -1: 
            match.home_b365 = get_float_val(sheet.cell(r,b365w_id).value)
        if b365w_id != -1:
            match.away_b365 = get_float_val(sheet.cell(r,b365l_id).value)
        if psw_id != -1:
            match.home_ps = get_float_val(sheet.cell(r,psw_id).value)
        if psl_id != -1:
            match.away_ps = get_float_val(sheet.cell(r,psl_id).value)
        if avgw_id != -1:
            match.home_avg = get_float_val(sheet.cell(r,avgw_id).value)
        if avgl_id != -1:
            match.away_avg = get_float_val(sheet.cell(r,avgl_id).value)
        if maxw_id != -1:
            match.home_max = get_float_val(sheet.cell(r,maxw_id).value)
        if maxl_id != -1:
            match.away_max = get_float_val(sheet.cell(r,maxl_id).value)

        match.save()
    return []

def load_xlsx_wta(filepath):
    # dirname = os.path.dirname(__file__)
    # filename = os.path.join(dirname, 'atp/2019.xlsx')
    book = xlrd.open_workbook(filepath)
    sheet = book.sheet_by_index(0)
    harr = []
    for c in range(1, sheet.ncols):
        harr.append(sheet.cell(0,c).value)

    b365w_id =  harr.index("B365W") + 1
    b365l_id =  harr.index("B365L") + 1
    maxw_id =  harr.index("MaxW") + 1
    maxl_id =  harr.index("MaxL") + 1
    psw_id =  harr.index("PSW") + 1
    psl_id =  harr.index("PSL") + 1
    avgw_id = harr.index("AvgW") + 1
    avgl_id = harr.index("AvgL") + 1

    for r in range(1, sheet.nrows):
        match = WTAMatch()
        match.location	= sheet.cell(r,1).value
        match.tournament	= sheet.cell(r,2).value
        _date	= sheet.cell(r,3).value
        match.date = datetime.datetime(*xlrd.xldate_as_tuple(_date, book.datemode))
        
        match.round = sheet.cell(r,7).value    
        match.bestof = int(sheet.cell(r,8).value)    
        match.winner = sheet.cell(r,9).value
        match.loser = sheet.cell(r,10).value
        match.home  = find_player_wta(sheet.cell(r,9).value)
        match.away = find_player_wta(sheet.cell(r,10).value)
        dup_match = find_duplicate_wta(match.winner, match.loser, match.date)
        if dup_match is not None:
            continue

        match.court = sheet.cell(r,5).value
        match.surface = sheet.cell(r,6).value
        # match.wrank = sheet.cell(r,11).value
        # match.lrank = sheet.cell(r,12).value
        # match.wpts = sheet.cell(r,13).value
        # match.lpts = sheet.cell(r,14).value
    
        match.home_r1 = get_int_val(sheet.cell(r,15).value)
        match.away_r1 = get_int_val(sheet.cell(r,16).value)
        match.home_r2 = get_int_val(sheet.cell(r,17).value)
        match.away_r2 = get_int_val(sheet.cell(r,18).value)
        match.home_r3 = get_int_val(sheet.cell(r,19).value)
        match.away_r3 = get_int_val(sheet.cell(r,20).value)
        match.home_winsets = get_int_val(sheet.cell(r,21).value)
        match.away_winsets = get_int_val(sheet.cell(r,22).value)
        match.totalsets = match.home_winsets + match.away_winsets
        match.status = sheet.cell(r,23).value
        if b365w_id != -1: 
            match.home_b365 = get_float_val(sheet.cell(r,b365w_id).value)
        if b365w_id != -1:
            match.away_b365 = get_float_val(sheet.cell(r,b365l_id).value)
        if psw_id != -1:
            match.home_ps = get_float_val(sheet.cell(r,psw_id).value)
        if psl_id != -1:
            match.away_ps = get_float_val(sheet.cell(r,psl_id).value)
        if avgw_id != -1:
            match.home_avg = get_float_val(sheet.cell(r,avgw_id).value)
        if avgl_id != -1:
            match.away_avg = get_float_val(sheet.cell(r,avgl_id).value)
        if maxw_id != -1:
            match.home_max = get_float_val(sheet.cell(r,maxw_id).value)
        if maxl_id != -1:
            match.home_min = get_float_val(sheet.cell(r,maxl_id).value)

        match.save()
    return []

def import_atp_match(request):
    dirname = os.path.dirname(__file__)
    atp_path = os.path.join(dirname, 'atp')
    atpfiles = []
    for r, d, f in os.walk(atp_path):
        for file in f:
            if '.xlsx' in file:
                atpfiles.append(os.path.join(r, file))

    for f in atpfiles:
        load_xlsx_atp(f)

    context = {
        "file_list": atpfiles,
    }
    return render(request, 'match/file_list.html', context)

def import_wta_match(request):
    dirname = os.path.dirname(__file__)
    wta_path = os.path.join(dirname, 'wta')
    wtafiles = []
    for r, d, f in os.walk(wta_path):
        for file in f:
            if '.xlsx' in file:
                wtafiles.append(os.path.join(r, file))

    for f in wtafiles:
        load_xlsx_wta(f)

    context = {
        "file_list": wtafiles,
    }
    return render(request, 'match/file_list.html', context)

def change_winna_to_max(request):
    matches = ATPMatch.objects.all()
    for match in matches:
        tmp_home = match.home_winamax 
        tmp_away = match.away_winamax
        match.home_max = tmp_home
        match.away_max = tmp_away
        match.home_winamax = -1
        match.away_winamax = -1
        match.save()
    
    matches = ATPMatch.objects.all()
    for match in matches:
        tmp_home = match.home_winamax 
        tmp_away = match.away_winamax
        match.home_max = tmp_home
        match.away_max = tmp_away
        match.home_winamax = -1
        match.away_winamax = -1
        match.save()
    return HttpResponse("<h1> Very good! </h1>")
    
# Find the atp player with name
def find_player(str):
    str = str.upper()
    players = ATPPlayer.objects.filter(nicknames__contains=str)
    if len(players) > 0:
        player = players[0]
        return player.name
    else:
        return ""

#Fine the atp match with winner loser, date
def find_duplicate(winner, loser, date):
    players = ATPMatch.objects.filter(winner=winner, loser=loser, date=date)
    if len(players) > 0:
        return players[0]
    else:
        return None

#Fine the wta player
def find_player_wta(str):
    str = str.upper()
    players = WTAPlayer.objects.filter(nicknames__contains=str)
    if len(players) > 0:
        player = players[0]
        return player.name
    else:
        return ""

#Fine the duplicate of WTA
def find_duplicate_wta(winner, loser, date):
    players = WTAMatch.objects.filter(winner=winner, loser=loser, date=date)
    if len(players) > 0:
        return players[0]
    else:
        return None

def get_int_val(num):
    result = 0
    if num == '':
        result = -1
    else:
        result = int(num)
    return result
def get_float_val(num):
    result = 0
    if num == '':
        result = -1
        return -1
    else:
        result = num
        return num
    return result
