import scrapy
import re
from sports_scrapy.items import AtpPlayerItem, WtaPlayerItem
#Beatiful Soup - To parse the html
from bs4 import BeautifulSoup
from time import sleep
import time

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

class AtpPlayerSpider(scrapy.Spider):
    pipelines = ["atpplayer"]
    name = 'atpplayer'
    start_urls = [
        'https://live-tennis.eu/fr/classement-atp-live',
    ]

    def parse(self, response):
        player_rows = response.xpath('//table[@id="u868"]/tbody/tr[@bgcolor and @class]')
        for player_item in player_rows:
        #rank
            rank_txt = player_item.xpath('./td[1]/text()').extract_first().strip()
            if rank_txt == '':
                rank = 1000
            else:
                rank = int(player_item.xpath('./td[1]/text()').extract_first().strip(), 10)
        #max_rank
            mc = player_item.xpath('./td[2]/b[2]/text()').extract_first().strip()
            if bool(re.match('^(?=.*[a-zA-Z-])', mc)) != True:
                max_rank = int(mc,10)
            elif mc.find('CH') != -1 or mc.find('MC') != -1: 
                max_rank = rank
        #name
            origin_name = player_item.xpath('./td[4]/text()').extract_first().strip()
            name = get_formatted_name(origin_name)
        #age
            age_txt = player_item.xpath('./td[5]/text()').extract_first().strip()
            age = int(age_txt)
        #country
            country = player_item.xpath('./td[6]/text()').extract_first().strip()
        #pts
            pts_txt = player_item.xpath('./td[7]/text()').extract_first().strip()
            pts = int(pts_txt)
        #next_pts
            next_pts_txt = player_item.xpath('./td[13]/text()').extract_first().strip()
            next_pts = get_pts_int(next_pts_txt)
        #max_pts
            max_pts_txt = player_item.xpath('./td[14]/text()').extract_first().strip()
            max_pts = get_pts_int(max_pts_txt)
        #nicknames
            nickname = get_eng_name(origin_name)
            
            item = AtpPlayerItem()
            item['rank'] = rank
            item['name'] = name
            item['nicknames'] = '#' + item['name'] + '#' + origin_name + '#' + nickname
            item['max_rank'] = max_rank
            item['age'] = age
            item['country'] = country
            item['pts'] = pts
            item['next_pts'] = next_pts
            item['max_pts'] = max_pts
            yield item

class WtaPlayerSpider(scrapy.Spider):
    pipelines = ["wtaplayer"]
    name = 'wtaplayer'
    start_urls = [
        'https://live-tennis.eu/fr/classement-wta-officiel',
    ]

    def parse(self, response):
        player_rows = response.xpath('//table[@id="u868"]/tbody/tr[@bgcolor and @class]')
        for player_item in player_rows:
        #rank
            rank_txt = player_item.xpath('./td[1]/text()').extract_first().strip()
            if rank_txt == '':
                rank = 1000
            else:
                rank = int(rank_txt, 10)

        #name
            origin_name = player_item.xpath('./td[3]/text()').extract_first().strip()
            name = get_formatted_name(origin_name)
        #age
            age_txt = player_item.xpath('./td[4]/text()').extract_first().strip()
            age = int(age_txt)
        #country
            country = player_item.xpath('./td[5]/text()').extract_first().strip()
        #pts
            pts_txt = player_item.xpath('./td[6]/text()').extract_first().strip()
            pts = int(pts_txt)
        #next_pts
            next_pts_txt = player_item.xpath('./td[11]/text()').extract_first().strip()
            next_pts = get_pts_int(next_pts_txt)
        #max_pts
            max_pts_txt = player_item.xpath('./td[12]/text()').extract_first(default="-").strip()
            max_pts = get_pts_int(max_pts_txt)
        #nicknames
            nickname = get_eng_name(origin_name)
            
            item = WtaPlayerItem()
            item['rank'] = rank
            item['name'] = name
            item['nicknames'] = '#' + item['name'] + '#' + origin_name + '#' + nickname
            item['age'] = age
            item['country'] = country
            item['pts'] = pts
            item['next_pts'] = next_pts
            item['max_pts'] = max_pts
            yield item