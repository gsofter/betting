# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from players.models import ATPPlayer, WTAPlayer
from matches.models import ATPMatch, WTAMatch
from tournaments.models import ATPTournament,WTATournament

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
                home_player = ATPPlayer.objects.get(nicknames__contains=home)
                away_player = ATPPlayer.objects.get(nicknames__contains=away)
            
                if home_player is not None and away_player is not None:
                    item['home'] = home_player.name
                    item['away'] = away_player.name
                else:
                    print ('home or away player is not listed in the players list')
                    self.export_to_file(item)
                    return item
            except ATPPlayer.DoesNotExist:
                print('home or away player does not exist on the players list')
                self.export_to_file(item)
                return item
            
            match = ATPMatch.objects.get(home=item["home"], away=item['away'], date=item['date'])
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
                home_player = WTAPlayer.objects.get(nicknames__contains=home)
                away_player = WTAPlayer.objects.get(nicknames__contains=away)
            
                if home_player is not None and away_player is not None:
                    item['home'] = home_player.name
                    item['away'] = away_player.name
                else:
                    print ('home or away player is not listed in the players list')
                    self.export_to_file(item)
                    return item
            except WTAMatch.DoesNotExist:
                print('home or away player does not exist on the players list')
                self.export_to_file(item)
                return item
            
            match = WTAMatch.objects.get(home=item["home"], away=item['away'], date=item['date'])
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
