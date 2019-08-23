# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from players.models import ATPPlayer, WTAPlayer
from matches.models import ATPMatch, WTAMatch
from tournaments.models import ATPTournament,WTATournament
def get_pts_int(str):
    result = 0
    if str == '-':
        result = 0
    else:
        result = int(str, 10)
    return result
def get_eng_name(str):
    result = ''
    str = str.upper()
    for x in range(0, len(str)):
        ch = str[x].upper()
        if ch == 'Á' or ch == 'Â' or ch == 'À' or ch == 'Å' or ch == 'Ã' or ch == 'Ä' or ch == 'Ă':
            ch = 'A'
        if ch == 'Ç' or ch == 'Ć' or  ch == 'Č':
            ch = 'C'
        if ch == 'É' or ch == 'Ê' or ch == 'È' or ch == 'Ë' or ch == 'Ē' or ch == 'Ę':
            ch = 'E'
        if ch == 'Í' or ch == 'Î' or ch == 'Ì' or ch == 'Ï' or ch == 'İ':
            ch = 'I'
        if ch == 'Ñ' or ch == 'Ń':
            ch = 'N'
        if ch == 'Ó' or ch == 'Ô' or ch == 'Ò' or ch == 'Ø' or ch == 'Õ' or ch == 'Ö':
            ch = 'O'
        if ch == 'Š' or ch == 'Ś' or ch == 'Ș':
            ch = 'S'
        if ch == 'Ř':
            ch = 'R'
        if ch == 'Ð':			
            ch = 'D'
        if ch == 'Ú' or ch == 'Ü' or ch == 'Ů':
            ch = 'U'
        if ch == 'Ý':
            ch = 'Y'
        if ch == 'Ž' or ch == 'Ż':
            ch = 'Z'
        result += ch
    return result

def get_formatted_name(str):
    pos = str.index(' ')
    surname = str[:pos-1]
    familyname = str[pos+1:]
    tstr = familyname + ' ' + surname[0] + '.'
    tstr = tstr.upper()
    result = ''
    for x in range(0, len(tstr)):
        ch = tstr[x]
        if ch == 'Á' or ch == 'Â' or ch == 'À' or ch == 'Å' or ch == 'Ã' or ch == 'Ä' or ch == 'Ă':
            ch = 'A'
        if ch == 'Ç' or ch == 'Ć' or  ch == 'Č':
            ch = 'C'
        if ch == 'É' or ch == 'Ê' or ch == 'È' or ch == 'Ë' or ch == 'Ē' or ch == 'Ę':
            ch = 'E'
        if ch == 'Í' or ch == 'Î' or ch == 'Ì' or ch == 'Ï' or ch == 'İ':
            ch = 'I'
        if ch == 'Ñ' or ch == 'Ń':
            ch = 'N'
        if ch == 'Ó' or ch == 'Ô' or ch == 'Ò' or ch == 'Ø' or ch == 'Õ' or ch == 'Ö':
            ch = 'O'
        if ch == 'Š' or ch == 'Ś' or ch == 'Ș':
            ch = 'S'
        if ch == 'Ř':
            ch = 'R'
        if ch == 'Ð':			
            ch = 'D'
        if ch == 'Ú' or ch == 'Ü' or ch == 'Ů':
            ch = 'U'
        if ch == 'Ý':
            ch = 'Y'
        if ch == 'Ž' or ch == 'Ż':
            ch = 'Z'
        result += ch
    return result

class AtpPlayerScrapyPipeline(object):
    def process_item(self, item, spider):
        if 'atpplayer' not in getattr(spider, 'pipelines', []):
            return item
        try:
            player = ATPPlayer.objects.get(name=item["name"])
            print (player.name + " already exist")
            player.rank = item['rank']
            player.name = item['name']
            player.nicknames = item['nicknames']
            player.max_rank = item['max_rank']
            player.age = item['age']
            player.country = item['country']
            player.pts = item['pts']
            player.next_pts = item['next_pts']
            player.max_pts = item['max_pts']
            player.save()
            return item
        except ATPPlayer.DoesNotExist:
            pass
        item.save()
        return item

class WtaPlayerScrapyPipeline(object):
    def process_item(self, item, spider):
        if 'wtaplayer' not in getattr(spider, 'pipelines', []):
            return item
        try:
            player = WTAPlayer.objects.get(name=item["name"])
            print (player.name + " already exist")
            player.rank = item['rank']
            player.name = item['name']
            player.age = item['age']
            player.country = item['country']
            player.pts = item['pts']
            player.next_pts = item['next_pts']
            player.max_pts = item['max_pts']
            player.save()
            return item
        except WTAPlayer.DoesNotExist:
            pass
        item.save()
        return item

class AtpMatchScrapyPipeline(object):
    def process_item(self, item, spider):
        if 'atpmatch' not in getattr(spider, 'pipelines', []):
            return item
        try:
            home = item['home'].upper()
            away = item['away'].upper()
            try:
                home_player = ATPPlayer.objects.filter(nicknames__contains=home)
                away_player = ATPPlayer.objects.filter(nicknames__contains=away)
            
                if len(home_player) > 0 and len(away_player) > 0:
                    item['home'] = home_player[0].name
                    item['away'] = away_player[0].name
                else:
                    print ('home or away player is not listed in the players list')
                    self.export_to_file(item)
                    return item
            except ATPPlayer.DoesNotExist:
                print('home or away player does not exist on the players list')
                self.export_to_file(item)
                return item
            
            match = ATPMatch.objects.get(home=item["home"], away=item['away'])
            print (match.home + 'vs'+ match.away + match.date.strftime('%d-%b-%Y')  + " already exist")
            match.round = item['round']
            match.date = item['date']
            match.home = item['home']
            match.away = item['away']
            match.location = item['location']
            match.tournament = item['tournament']
            match.winner = item['winner']
            match.loser = item['loser']
            match.status = item['status']
            match.comment = item['comment']
            match.home_r1 = item['home_r1']
            match.home_r2 = item['home_r2']
            match.home_r3 = item['home_r3']
            match.home_r4 = item['home_r4']
            match.home_r5 = item['home_r5']
            match.away_r1 = item['away_r1']
            match.away_r2 = item['away_r2']
            match.away_r3 = item['away_r3']
            match.away_r4 = item['away_r4']
            match.away_r5 = item['away_r5']
            match.home_winsets = item['home_winsets']
            match.home_winsets = item['home_winsets']
            match.save()
            return item
        except ATPMatch.DoesNotExist:
            pass
        item.save()
        return item
    def export_to_file(self, item):
        file = open('players.txt', 'a+')
        file.write(item['home'] + "\r\n")
        file.write(item['away'] + "\r\n")
        file.close()

class WtaMatchScrapyPipeline(object):
    def process_item(self, item, spider):
        if 'wtamatch' not in getattr(spider, 'pipelines', []):
            return item
        try:
            home = item['home'].upper()
            away = item['away'].upper()
            try:
                home_player = WTAPlayer.objects.filter(nicknames__contains=home)
                away_player = WTAPlayer.objects.filter(nicknames__contains=away)
            
                if len(home_player) > 0 and len(away_player) > 0:
                    item['home'] = home_player[0].name
                    item['away'] = away_player[0].name
                else:
                    print ('home or away player is not listed in the players list')
                    self.export_to_file(item)
                    return item
            except WTAMatch.DoesNotExist:
                print('home or away player does not exist on the players list')
                self.export_to_file(item)
                return item
            
            match = WTAMatch.objects.get(home=item["home"], away=item['away'])
            print (match.home + 'vs'+ match.away + match.date.strftime('%d-%b-%Y')  + " already exist")
            match.round = item['round']
            match.date = item['date']
            match.home = item['home']
            match.away = item['away']
            match.location = item['location']
            match.tournament = item['tournament']
            match.winner = item['winner']
            match.loser = item['loser']
            match.status = item['status']
            match.comment = item['comment']
            match.home_r1 = item['home_r1']
            match.home_r2 = item['home_r2']
            match.home_r3 = item['home_r3']
            match.home_r4 = item['home_r4']
            match.home_r5 = item['home_r5']
            match.away_r1 = item['away_r1']
            match.away_r2 = item['away_r2']
            match.away_r3 = item['away_r3']
            match.away_r4 = item['away_r4']
            match.away_r5 = item['away_r5']
            match.home_winsets = item['home_winsets']
            match.home_winsets = item['home_winsets']
            match.save()
            return item
        except WTAMatch.DoesNotExist:
            pass
        item.save()
        return item
    def export_to_file(self, item):
        file = open('wtaplayers.txt', 'a+')
        file.write(item['home'] + "\r\n")
        file.write(item['away'] + "\r\n")
        file.close()

class AtpTournamentScrapyPipeline(object):
    def process_item(self, item, spider):
        if 'atptournament' not in getattr(spider, 'pipelines', []):
            return item
        try:
            tour_name = item['name'].upper()
            old_tournament = ATPTournament.objects.get(nicknames__contains=tour_name)

            if old_tournament is not None and away_player is not None:
                old_tournament.round = item['round']
                old_tournament.name = item['name']
                old_tournament.date = item['name']
                old_tournament.location = item['name']
                old_tournament.surface = item['surface']
                old_tournament.series = item['series']
                old_tournament.price = item['price']
                old_tournament.save()
            else:
                item.save()
        except:
            item.save()
            pass
        return item

class WtaTournamentScrapyPipeline(object):
    def process_item(self, item, spider):
        if 'wtatournament' not in getattr(spider, 'pipelines', []):
            return item
        try:
            tour_name = item['name'].upper()
            old_tournament = WTATournament.objects.get(nicknames__contains=tour_name)

            if old_tournament is not None and away_player is not None:
                old_tournament.round = item['round']
                old_tournament.name = item['name']
                old_tournament.date = item['name']
                old_tournament.location = item['name']
                old_tournament.surface = item['surface']
                old_tournament.series = item['series']
                old_tournament.price = item['price']
                old_tournament.save()
            else:
                item.save()
        except:
            item.save()
            pass
        return item

class AtpPerformScrapyPipeline(object):
    def process_item(self, item, spider):
        if 'atpperform' not in getattr(spider, 'pipelines', []):
            return item
        try:
            if len(item) == 0:
                return []
            home = item['home'].upper()
            away = item['away'].upper()
            try:
                home_player = ATPPlayer.objects.filter(nicknames__contains=home)
                away_player = ATPPlayer.objects.filter(nicknames__contains=away)
            
                if len(home_player) > 0 and len(away_player) > 0:
                    item['home'] = home_player[0].name
                    item['away'] = away_player[0].name
                else:
                    print ('home or away player is not listed in the players list')
                    self.export_to_file(item)
                    return item
            except ATPPlayer.DoesNotExist:
                print('home or away player does not exist on the players list')
                self.export_to_file(item)
                return item
            match = ATPMatch.objects.get(home=item["home"], away=item['away'])   
            match.home_aces = item['home_aces']
            match.home_doublefault = item['home_doublefault']
            match.home_total = item['home_total']
            match.home_ser = item['home_ser']
            match.home_ser1 = item['home_ser1']
            match.home_ser2 = item['home_ser2']
            match.home_rec = item['home_rec']
            match.away_aces = item['away_aces']
            match.away_doublefault = item['away_doublefault']
            match.away_total = item['away_total']
            match.away_ser = item['away_ser']
            match.away_ser1 = item['away_ser1']
            match.away_ser2 = item['away_ser2']
            match.away_rec = item['away_rec']
            match.save()
        except ATPMatch.DoesNotExist:
            pass
        match = ATPMatch()
        match.status = 'fin'
        match.home = item['home']
        match.away = item['away']
        match.date = item['date']
        match.home_aces = item['home_aces']
        match.home_doublefault = item['home_doublefault']
        match.home_total = item['home_total']
        match.home_ser = item['home_ser']
        match.home_ser1 = item['home_ser1']
        match.home_ser2 = item['home_ser2']
        match.home_rec = item['home_rec']
        match.away_aces = item['away_aces']
        match.away_doublefault = item['away_doublefault']
        match.away_total = item['away_total']
        match.away_ser = item['away_ser']
        match.away_ser1 = item['away_ser1']
        match.away_ser2 = item['away_ser2']
        match.away_rec = item['away_rec']
        match.save()
        return item

    def export_to_file(self, item):
        file = open('players.txt', 'a+')
        file.write(item['home'] + "\r\n")
        file.write(item['away'] + "\r\n")
        file.close()

class WtaPerformScrapyPipeline(object):
    def process_item(self, item, spider):
        if 'wtaperform' not in getattr(spider, 'pipelines', []):
            return item
        try:
            if len(item) == 0:
                return []
            home = item['home'].upper()
            away = item['away'].upper()
            try:
                home_player = WTAPlayer.objects.filter(nicknames__contains=home)
                away_player = WTAPlayer.objects.filter(nicknames__contains=away)
            
                if len(home_player) > 0 and len(away_player) > 0:
                    item['home'] = home_player[0].name
                    item['away'] = away_player[0].name
                else:
                    print ('home or away player is not listed in the players list')
                    self.export_to_file(item)
                    return item
            except WTAPlayer.DoesNotExist:
                print('home or away player does not exist on the players list')
                self.export_to_file(item)
                return item
            match = WTAMatch.objects.get(home=item["home"], away=item['away'])
            match.home_aces = item['home_aces']
            match.home_doublefault = item['home_doublefault']
            match.home_total = item['home_total']
            match.home_ser = item['home_ser']
            match.home_ser1 = item['home_ser1']
            match.home_ser2 = item['home_ser2']
            match.home_rec = item['home_rec']
            match.away_aces = item['away_aces']
            match.away_doublefault = item['away_doublefault']
            match.away_total = item['away_total']
            match.away_ser = item['away_ser']
            match.away_ser1 = item['away_ser1']
            match.away_ser2 = item['away_ser2']
            match.away_rec = item['away_rec']
            match.save()
        except WTAMatch.DoesNotExist:
            pass
        match = WTAMatch()
        match.status = 'fin'
        match.home = item['home']
        match.away = item['away']
        match.date = item['date']
        match.home_aces = item['home_aces']
        match.home_doublefault = item['home_doublefault']
        match.home_total = item['home_total']
        match.home_ser = item['home_ser']
        match.home_ser1 = item['home_ser1']
        match.home_ser2 = item['home_ser2']
        match.home_rec = item['home_rec']
        match.away_aces = item['away_aces']
        match.away_doublefault = item['away_doublefault']
        match.away_total = item['away_total']
        match.away_ser = item['away_ser']
        match.away_ser1 = item['away_ser1']
        match.away_ser2 = item['away_ser2']
        match.away_rec = item['away_rec']
        match.save()
        return item

    def export_to_file(self, item):
        file = open('players.txt', 'a+')
        file.write(item['home'] + "\r\n")
        file.write(item['away'] + "\r\n")
        file.close()

class AtpOddScrapyPipeline(object):
    def process_item(self, item, spider):
        if 'atpodd' not in getattr(spider, 'pipelines', []):
            return item
        try:
            if len(item) == 0:
                return []
            home = item['home'].upper()
            away = item['away'].upper()
            try:
                home_player = ATPPlayer.objects.filter(nicknames__contains=home)
                away_player = ATPPlayer.objects.filter(nicknames__contains=away)
            
                if len(home_player) > 0 and len(away_player) > 0:
                    item['home'] = home_player[0].name
                    item['away'] = away_player[0].name
                else:
                    print ('home or away player is not listed in the players list')
                    self.export_to_file(item)
                    return item
            except ATPPlayer.DoesNotExist:
                print('home or away player does not exist on the players list')
                self.export_to_file(item)
                return item
            match = ATPMatch.objects.get(home=item["home"], away=item['away'])
            match.home_unibet = item['ubhome']
            match.home_betclic = item['bchome']
            match.home_winamax = item['maxhome']
            match.home_b365 = item['ubhome']

            match.away_unibet = item['ubaway']
            match.away_betclic = item['bcaway']
            match.away_winamax = item['maxaway']
            match.home_b365 = item['bcaway']
            
            match.save()
        except ATPMatch.DoesNotExist:
            pass
        
        return item

    def export_to_file(self, item):
        file = open('players.txt', 'a+')
        file.write(item['home'] + "\r\n")
        file.write(item['away'] + "\r\n")
        file.close()

class WtaOddScrapyPipeline(object):
    def process_item(self, item, spider):
        if 'wtaodd' not in getattr(spider, 'pipelines', []):
            return item
        try:
            if len(item) == 0:
                return []
            home = item['home'].upper()
            away = item['away'].upper()
            try:
                home_player = WTAPlayer.objects.filter(nicknames__contains=home)
                away_player = WTAPlayer.objects.filter(nicknames__contains=away)
            
                if len(home_player) > 0 and len(away_player) > 0:
                    item['home'] = home_player[0].name
                    item['away'] = away_player[0].name
                else:
                    print ('home or away player is not listed in the players list')
                    self.export_to_file(item)
                    return item
            except WTAPlayer.DoesNotExist:
                print('home or away player does not exist on the players list')
                self.export_to_file(item)
                return item
            match = WTAMatch.objects.get(home=item["home"], away=item['away'])
            match.home_unibet = item['ubhome']
            match.home_betclic = item['bchome']
            match.home_winamax = item['maxhome']
            
            match.away_unibet = item['ubaway']
            match.away_betclic = item['bcaway']
            match.away_winamax = item['maxaway']
            
            match.save()
        except WTAMatch.DoesNotExist:
            pass
        
        return item

    def export_to_file(self, item):
        file = open('players.txt', 'a+')
        file.write(item['home'] + "\r\n")
        file.write(item['away'] + "\r\n")
        file.close()
