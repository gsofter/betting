import scrapy
import re
from sports_scrapy.items import AtpMatchItem,WtaMatchItem

from time import sleep
import time
from  datetime import datetime

def get_teamname_from_str(str):
    teamname = ''
    try:
        _id = str.index('(')
        teamname = str[:_id-1]
    except:
        teamname = str
    return teamname

def get_score_from_str(str):
    val = -1
    if str != '-':
        val = int(str, 10)
    return val
    
class AtpMatchSpider(scrapy.Spider):
    pipelines = ['atpmatch']
    name = 'atpmatch'
    start_urls = [
        'https://www.xscores.com/tennis/',
    ]

    def parse(self, response):
        try:
            atp_match_rows = response.xpath("//div[@id='scoreTableDiv']//div[@id and contains(@class, 'match_line') and @data-country-name='ATP-S']")
            for match_item in atp_match_rows:
            #date and time
                time_str = match_item.xpath(".//div[@id='ko_time']/text()").extract_first().strip()
                date_str = match_item.xpath("./@data-matchday").extract_first()
                date = datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M')
            #round
                round = match_item.xpath('./@data-league-round').extract_first().strip()
            
            #home
                str = match_item.xpath('./@data-home-team').extract_first().strip()
                home = get_teamname_from_str(str)
            #away
                str = match_item.xpath('.//div[@class="score_away_txt score_cell wrap"]/span/text()').extract_first(default="not-found").strip()
                if str == "not-found":
                    str = match_item.xpath('.//div[@class="score_away_txt score_cell wrap"]/span/b/text()').extract_first(default="not-found").strip()
                away = get_teamname_from_str(str)
            #tournament and location
                _t = match_item.xpath('./@data-league-name').extract_first().strip()
                tournament = _t.split(' ')[0]
                location = _t.split(' ')[1]

            #match_status and comment
                match_status = match_item.xpath('./@data-statustype').extract_first().strip()
                # match_comment = match_item.xpath('./@data-statustype').extract_first().strip()
                #if the match is the upcoming match
                if match_status == 'sched':
                    item = AtpMatchItem()
                    item['home'] = home
                    item['away'] = away
                    item['date'] = date
                #common fields
                    item['round'] = round
                    item['winner'] = winner
                    item['loser'] = loser
                    item['tournament'] = tournament
                    item['location'] = location
                    item['comment'] = match_status
                    item['status'] = match_status
                    item['totalgames'] = totalgames
                    item['bestof'] = 3
                #home player fields
                    item['home_r1'] = -1
                    item['home_r2'] = -1
                    item['home_r3'] = -1
                    item['home_r4'] = -1
                    item['home_r5'] = -1
                    item['home_winsets'] = -1
                #away player fields
                    item['away_r1'] = -1
                    item['away_r2'] = -1
                    item['away_r3'] = -1
                    item['away_r4'] = -1
                    item['away_r5'] = -1
                    item['away_winsets'] = -1
                    yield item
                    continue
            #winsets
                home_winsets = match_item.xpath(".//div[contains(@class,'score_ft score_cell')]/div[1]/text()").extract_first().strip()
                away_winsets = match_item.xpath(".//div[contains(@class,'score_ft score_cell')]/div[2]/text()").extract_first().strip()
                if home_winsets > away:
                    winner = home
                    loser = away
                else:
                    winner = away
                    loser = home
            #round scores    
                home_r1_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][1]/div[1]/text()").extract_first().strip()
                home_r2_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][2]/div[1]/text()").extract_first().strip()
                home_r3_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][3]/div[1]/text()").extract_first().strip()
                home_r4_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][4]/div[1]/text()").extract_first().strip()
                home_r5_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][5]/div[1]/text()").extract_first().strip()

                away_r1_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][1]/div[2]/text()").extract_first().strip()
                away_r2_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][2]/div[2]/text()").extract_first().strip()
                away_r3_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][3]/div[2]/text()").extract_first().strip()
                away_r4_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][4]/div[2]/text()").extract_first().strip()
                away_r5_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][5]/div[2]/text()").extract_first().strip()
                
                home_r1 = get_score_from_str(home_r1_t)
                home_r2 = get_score_from_str(home_r2_t)
                home_r3 = get_score_from_str(home_r3_t)
                home_r4 = get_score_from_str(home_r4_t)
                home_r5 = get_score_from_str(home_r5_t)

                away_r1 = get_score_from_str(away_r1_t)
                away_r2 = get_score_from_str(away_r2_t)
                away_r3 = get_score_from_str(away_r3_t)
                away_r4 = get_score_from_str(away_r4_t)
                away_r5 = get_score_from_str(away_r5_t)
            #total games    
                totalgames = 0
                if home_r5 != -1 and away_r5 != -1:
                    totalgames += home_r5 + away_r5 
                if home_r4 != -1 and away_r4 != -1:
                    totalgames += home_r4 + away_r4 
                if home_r3 != -1 and away_r3 != -1:
                    totalgames += home_r3 + away_r3 
                if home_r2 != -1 and away_r2 != -1:
                    totalgames += home_r2 + away_r2 
                if home_r1 != -1 and away_r1 != -1:
                    totalgames += home_r1 + away_r1
        
                item = AtpMatchItem()
                item['home'] = home
                item['away'] = away
                item['date'] = date
            #common fields
                item['round'] = round
                item['winner'] = winner
                item['loser'] = loser
                item['tournament'] = tournament
                item['location'] = location
                item['comment'] = match_status
                item['status'] = match_status
                item['totalgames'] = totalgames
                item['bestof'] = 3
            #home fields
                item['home_r1'] = home_r1
                item['home_r2'] = home_r2
                item['home_r3'] = home_r3
                item['home_r4'] = home_r4
                item['home_r5'] = home_r5
                item['home_winsets'] = home_winsets
            #away fields
                item['away_r1'] = away_r1
                item['away_r2'] = away_r2
                item['away_r3'] = away_r3
                item['away_r4'] = away_r4
                item['away_r5'] = away_r5
                item['away_winsets'] = away_winsets
                yield item
        except:
            pass

class WtaMatchSpider(scrapy.Spider):
    pipelines = ['wtamatch']
    name = 'wtamatch'
    start_urls = [
        'https://www.xscores.com/tennis/',
    ]

    def parse(self, response):
        try:
            wta_match_rows = response.xpath("//div[@id='scoreTableDiv']//div[@id and contains(@class, 'match_line') and @data-country-name='WTA-S']")
            for match_item in wta_match_rows:
            #date and time
                time_str = match_item.xpath(".//div[@id='ko_time']/text()").extract_first().strip()
                date_str = match_item.xpath("./@data-matchday").extract_first()
                date = datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M')
            #round
                round = match_item.xpath('./@data-league-round').extract_first().strip()
            #home
                str = match_item.xpath('./@data-home-team').extract_first().strip()
                home = get_teamname_from_str(str)
            #away
                str = match_item.xpath('.//div[@class="score_away_txt score_cell wrap"]/span/text()').extract_first(default="not-found").strip()
                if str == "not-found":
                    str = match_item.xpath('.//div[@class="score_away_txt score_cell wrap"]/span/b/text()').extract_first(default="not-found").strip()
                away = get_teamname_from_str(str)
            #tournament and location
                _t = match_item.xpath('./@data-league-name').extract_first().strip()
                tournament = _t.split(' ')[0]
                location = _t.split(' ')[1]

            #match_status and comment
                match_status = match_item.xpath('./@data-statustype').extract_first().strip()
                # match_comment = match_item.xpath('./@data-statustype').extract_first().strip()
                #if the match is the upcoming match
                if match_status == 'sched':
                    item = WtaMatchItem()
                    item['home'] = home
                    item['away'] = away
                    item['date'] = date
                #common fields
                    item['round'] = round
                    item['winner'] = winner
                    item['loser'] = loser
                    item['tournament'] = tournament
                    item['location'] = location
                    item['comment'] = match_status
                    item['status'] = match_status
                    item['totalgames'] = totalgames
                    item['bestof'] = 3
                #home player fields
                    item['home_r1'] = -1
                    item['home_r2'] = -1
                    item['home_r3'] = -1
                    item['home_r4'] = -1
                    item['home_r5'] = -1
                    item['home_winsets'] = -1
                #away player fields
                    item['away_r1'] = -1
                    item['away_r2'] = -1
                    item['away_r3'] = -1
                    item['away_r4'] = -1
                    item['away_r5'] = -1
                    item['away_winsets'] = -1
                    yield item
                    continue
            #winsets
                home_winsets = match_item.xpath(".//div[contains(@class,'score_ft score_cell')]/div[1]/text()").extract_first().strip()
                away_winsets = match_item.xpath(".//div[contains(@class,'score_ft score_cell')]/div[2]/text()").extract_first().strip()
                if home_winsets > away:
                    winner = home
                    loser = away
                else:
                    winner = away
                    loser = home
            #round scores    
                home_r1_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][1]/div[1]/text()").extract_first().strip()
                home_r2_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][2]/div[1]/text()").extract_first().strip()
                home_r3_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][3]/div[1]/text()").extract_first().strip()
                home_r4_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][4]/div[1]/text()").extract_first().strip()
                home_r5_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][5]/div[1]/text()").extract_first().strip()

                away_r1_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][1]/div[2]/text()").extract_first().strip()
                away_r2_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][2]/div[2]/text()").extract_first().strip()
                away_r3_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][3]/div[2]/text()").extract_first().strip()
                away_r4_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][4]/div[2]/text()").extract_first().strip()
                away_r5_t = match_item.xpath(".//div[contains(@class,'score_ht score_cell')][5]/div[2]/text()").extract_first().strip()
                
                home_r1 = get_score_from_str(home_r1_t)
                home_r2 = get_score_from_str(home_r2_t)
                home_r3 = get_score_from_str(home_r3_t)
                home_r4 = get_score_from_str(home_r4_t)
                home_r5 = get_score_from_str(home_r5_t)

                away_r1 = get_score_from_str(away_r1_t)
                away_r2 = get_score_from_str(away_r2_t)
                away_r3 = get_score_from_str(away_r3_t)
                away_r4 = get_score_from_str(away_r4_t)
                away_r5 = get_score_from_str(away_r5_t)
            #total games    
                totalgames = 0
                if home_r5 != -1 and away_r5 != -1:
                    totalgames += home_r5 + away_r5 
                if home_r4 != -1 and away_r4 != -1:
                    totalgames += home_r4 + away_r4 
                if home_r3 != -1 and away_r3 != -1:
                    totalgames += home_r3 + away_r3 
                if home_r2 != -1 and away_r2 != -1:
                    totalgames += home_r2 + away_r2 
                if home_r1 != -1 and away_r1 != -1:
                    totalgames += home_r1 + away_r1
        
                item = WtaMatchItem()
                item['home'] = home
                item['away'] = away
                item['date'] = date
            #common fields
                item['round'] = round
                item['winner'] = winner
                item['loser'] = loser
                item['tournament'] = tournament
                item['location'] = location
                item['comment'] = match_status
                item['status'] = match_status
                item['totalgames'] = totalgames
                item['bestof'] = 3
            #home fields
                item['home_r1'] = home_r1
                item['home_r2'] = home_r2
                item['home_r3'] = home_r3
                item['home_r4'] = home_r4
                item['home_r5'] = home_r5
                item['home_winsets'] = home_winsets
            #away fields
                item['away_r1'] = away_r1
                item['away_r2'] = away_r2
                item['away_r3'] = away_r3
                item['away_r4'] = away_r4
                item['away_r5'] = away_r5
                item['away_winsets'] = away_winsets
                yield item
        except:
            pass

    