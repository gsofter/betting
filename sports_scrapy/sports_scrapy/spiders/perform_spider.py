import scrapy
import re
from sports_scrapy.items import AtpPerformItem, WtaPerformItem

from time import sleep
import time
from  datetime import datetime

class AtpPerformSpider(scrapy.Spider):
    pipelines = ['atpperform']
    name = 'atpperform'
    custom_settings = {
        'FEED_URI' : name + datetime.today().strftime("_%Y%m%d.csv"),
        'FEED_FORMAT' : 'csv',
    }

    start_urls = [
        'http://www.tennisendirect.net/hommes/australian-open-australia-wildcard-2019/',
        'http://www.tennisendirect.net/hommes/winston-salem-open-winston-salem-2019/',
        '',
    ]

    def parse(self, response):
        url = response.xpath('.//ul[@id="topmenu_full"]/li[3]/a/@href').extract_first().strip()
        yield scrapy.Request(url, callback=self.parse_list)
    
    def parse_list(self, response):
        matches = response.xpath('.//table[@id="table_live"]/tbody')
        print(str(len(matches)) + "!!!")
        for match in matches:
            home = match.xpath('.//tr[contains(@class, "pair")][1]/td[@class="match"]/a/text()').extract_first().strip()
            away = match.xpath('.//tr[contains(@class, "pair")][2]/td[@class="match"]/a/text()').extract_first().strip()
            date_str = match.xpath('.//tr[contains(@class, "pair")][1]/td[@rowspan="2"]/text()').extract_first().strip()
            date = datetime.strptime(date_str , '%d.%m.%y')
            # print(home + ' ' + away + ' ' + date.strftime("%d.%m.%y") + url)
            durl = match.xpath('.//tr[contains(@class, "pair")][1]/td[@rowspan="2"]/div/a/@href').extract_first().strip()
            print(home + ' ' + away + ' ' + date.strftime("%d.%m.%y") + durl)
            yield scrapy.Request(durl, callback=self.parse_detail)
    
    def parse_detail(self, response):
        try:
            date_div = response.xpath('.//div[@class="player_matches"][1]//table[@class="table_pmatches"]//tr[1]//td[1]/text()')
            if date_div is None:
                print("date_div is not none")
            date_str = response.xpath('.//div[@class="player_matches"][1]//table[@class="table_pmatches"]//tr[1]//td[1]/text()').extract_first().strip()
            date = self.get_time_from_string(date_str)
            table = response.xpath('.//div[@class="player_matches"]/table[@class="table_stats_match"][1]')
            if len(table) == 0:
                return []
            
            row_cnt = len(table.xpath('.//tr'))
            home = table.xpath('.//tr[1]/td[2]/a/text()').extract_first().strip()
            away = table.xpath('.//tr[1]/td[3]/a/text()').extract_first().strip()
            
            home_ser_txt = table.xpath('.//tr[2]/td[2]/text()').extract_first().strip()
            home_ser1_txt = table.xpath('.//tr[3]/td[2]/text()').extract_first().strip()
            home_ser2_txt = table.xpath('.//tr[4]/td[2]/text()').extract_first().strip()
            
            path_ace = './/tr[' + str(row_cnt) + ']/td[2]/text()'
            path_doublefault = './/tr[' + str(row_cnt-1) + ']/td[2]/text()'
            path_total = './/tr[' + str(row_cnt-2) + ']/td[2]/text()'
            path_rec = './/tr[' + str(row_cnt-3) + ']/td[2]/text()'
            home_aces_txt = table.xpath(path_ace).extract_first().strip()
            home_doublefault_txt = table.xpath(path_doublefault).extract_first().strip()
            home_total_txt = table.xpath(path_total).extract_first().strip()
            home_rec_txt = table.xpath(path_rec).extract_first().strip()
            
            home_aces = int(home_aces_txt,10)
            home_doublefault = int(home_doublefault_txt,10)
            home_ser = self.get_percent(home_ser_txt)
            home_ser1 = self.get_percent(home_ser1_txt)
            home_ser2 = self.get_percent(home_ser2_txt)
            home_rec = self.get_percent(home_rec_txt)
            home_total = self.get_percent(home_total_txt)

            away_ser_txt = table.xpath('.//tr[2]/td[3]/text()').extract_first().strip()
            away_ser1_txt = table.xpath('.//tr[3]/td[3]/text()').extract_first().strip()
            away_ser2_txt = table.xpath('.//tr[4]/td[3]/text()').extract_first().strip()
            
            path_ace = './/tr[' + str(row_cnt) + ']/td[3]/text()'
            path_doublefault = './/tr[' + str(row_cnt-1) + ']/td[3]/text()'
            path_total = './/tr[' + str(row_cnt-2) + ']/td[3]/text()'
            path_rec = './/tr[' + str(row_cnt-3) + ']/td[3]/text()'
            away_aces_txt = table.xpath(path_ace).extract_first().strip()
            away_doublefault_txt = table.xpath(path_doublefault).extract_first().strip()
            away_total_txt = table.xpath(path_total).extract_first().strip()
            away_rec_txt = table.xpath(path_rec).extract_first().strip()

            away_ser = self.get_percent(away_ser_txt)
            away_ser1 = self.get_percent(away_ser1_txt)
            away_ser2 = self.get_percent(away_ser2_txt)
            away_aces = int(away_aces_txt, 10)
            away_doublefault = int(away_doublefault_txt,10)
            away_total = self.get_percent(away_total_txt)
            away_rec = self.get_percent(away_rec_txt)

            item = AtpPerformItem()
            item['home'] = home
            item['away'] = away
            item['date'] = date
            item['home_aces'] = home_aces
            item['home_doublefault'] = home_doublefault
            item['home_total'] = home_total
            item['home_rec'] = home_rec
            item['home_ser'] = home_ser
            item['home_ser1'] = home_ser1
            item['home_ser2'] = home_ser2
            
            item['away_aces'] = away_aces
            item['away_doublefault'] = away_doublefault
            item['away_total'] = away_total
            item['away_rec'] = away_rec
            item['away_ser'] = away_ser
            item['away_ser1'] = away_ser1
            item['away_ser2'] = away_ser2
            yield item
        except:
            return []

    def get_percent(self, str):
        startid = str.index('(')+1
        endid = str.index('%')
        sstr = str[startid:endid]
        result = int(sstr, 10)
        return result
    def get_time_from_string(self, str):
        str = str.replace('.', ' ')
        str = str.replace(':', ' ')
        arr = str.split(' ')
        if len(arr) ==  5:
            resultdate = datetime.strptime(str, '%d %m %y %H %M')
        elif len(arr) == 3:
            resultdate = datetime.strptime(str, '%d %m %y')
        else:
            resultdate =datetime.today()
        return resultdate

class WtaPerformSpider(scrapy.Spider):
    pipelines = ['wtaperform']
    name = 'wtaperform'
    custom_settings = {
        'FEED_URI' : name + datetime.today().strftime("_%Y%m%d.csv"),
        'FEED_FORMAT' : 'csv',
    }
    start_urls = [
        'http://www.tennisendirect.net/femmes/connecticut-open-new-haven-2019/',
    ]

    def parse(self, response):
        url = response.xpath('.//ul[@id="topmenu_full"]/li[3]/a/@href').extract_first().strip()
        yield scrapy.Request(url, callback=self.parse_list)
    
    def parse_list(self, response):
        matches = response.xpath('.//table[@id="table_live"]/tbody')
        print(str(len(matches)) + "!!!")
        for match in matches:
            home = match.xpath('.//tr[contains(@class, "pair")][1]/td[@class="match"]/a/text()').extract_first().strip()
            away = match.xpath('.//tr[contains(@class, "pair")][2]/td[@class="match"]/a/text()').extract_first().strip()
            date_str = match.xpath('.//tr[contains(@class, "pair")][1]/td[@rowspan="2"]/text()').extract_first().strip()
            date = datetime.strptime(date_str , '%d.%m.%y')
            # print(home + ' ' + away + ' ' + date.strftime("%d.%m.%y") + url)
            durl = match.xpath('.//tr[contains(@class, "pair")][1]/td[@rowspan="2"]/div/a/@href').extract_first().strip()
            print(home + ' ' + away + ' ' + date.strftime("%d.%m.%y") + durl)
            yield scrapy.Request(durl, callback=self.parse_detail)
    
    def parse_detail(self, response):
        try:
            date_div = response.xpath('.//div[@class="player_matches"][1]//table[@class="table_pmatches"]//tr[1]//td[1]/text()')
            if date_div is None:
                print("date_div is not none")
            date_str = response.xpath('.//div[@class="player_matches"][1]//table[@class="table_pmatches"]//tr[1]//td[1]/text()').extract_first().strip()
            date = self.get_time_from_string(date_str)
            table = response.xpath('.//div[@class="player_matches"]/table[@class="table_stats_match"][1]')
            if len(table) == 0:
                return []
            
            row_cnt = len(table.xpath('.//tr'))
            home = table.xpath('.//tr[1]/td[2]/a/text()').extract_first().strip()
            away = table.xpath('.//tr[1]/td[3]/a/text()').extract_first().strip()
            
            home_ser_txt = table.xpath('.//tr[2]/td[2]/text()').extract_first().strip()
            home_ser1_txt = table.xpath('.//tr[3]/td[2]/text()').extract_first().strip()
            home_ser2_txt = table.xpath('.//tr[4]/td[2]/text()').extract_first().strip()
            
            path_ace = './/tr[' + str(row_cnt) + ']/td[2]/text()'
            path_doublefault = './/tr[' + str(row_cnt-1) + ']/td[2]/text()'
            path_total = './/tr[' + str(row_cnt-2) + ']/td[2]/text()'
            path_rec = './/tr[' + str(row_cnt-3) + ']/td[2]/text()'
            home_aces_txt = table.xpath(path_ace).extract_first().strip()
            home_doublefault_txt = table.xpath(path_doublefault).extract_first().strip()
            home_total_txt = table.xpath(path_total).extract_first().strip()
            home_rec_txt = table.xpath(path_rec).extract_first().strip()
            
            home_aces = int(home_aces_txt,10)
            home_doublefault = int(home_doublefault_txt,10)
            home_ser = self.get_percent(home_ser_txt)
            home_ser1 = self.get_percent(home_ser1_txt)
            home_ser2 = self.get_percent(home_ser2_txt)
            home_rec = self.get_percent(home_rec_txt)
            home_total = self.get_percent(home_total_txt)

            away_ser_txt = table.xpath('.//tr[2]/td[3]/text()').extract_first().strip()
            away_ser1_txt = table.xpath('.//tr[3]/td[3]/text()').extract_first().strip()
            away_ser2_txt = table.xpath('.//tr[4]/td[3]/text()').extract_first().strip()
            
            path_ace = './/tr[' + str(row_cnt) + ']/td[3]/text()'
            path_doublefault = './/tr[' + str(row_cnt-1) + ']/td[3]/text()'
            path_total = './/tr[' + str(row_cnt-2) + ']/td[3]/text()'
            path_rec = './/tr[' + str(row_cnt-3) + ']/td[3]/text()'
            away_aces_txt = table.xpath(path_ace).extract_first().strip()
            away_doublefault_txt = table.xpath(path_doublefault).extract_first().strip()
            away_total_txt = table.xpath(path_total).extract_first().strip()
            away_rec_txt = table.xpath(path_rec).extract_first().strip()

            away_ser = self.get_percent(away_ser_txt)
            away_ser1 = self.get_percent(away_ser1_txt)
            away_ser2 = self.get_percent(away_ser2_txt)
            away_aces = int(away_aces_txt, 10)
            away_doublefault = int(away_doublefault_txt,10)
            away_total = self.get_percent(away_total_txt)
            away_rec = self.get_percent(away_rec_txt)

            item = WtaPerformItem()
            item['home'] = home
            item['away'] = away
            item['date'] = date
            item['home_aces'] = home_aces
            item['home_doublefault'] = home_doublefault
            item['home_total'] = home_total
            item['home_rec'] = home_rec
            item['home_ser'] = home_ser
            item['home_ser1'] = home_ser1
            item['home_ser2'] = home_ser2
            
            item['away_aces'] = away_aces
            item['away_doublefault'] = away_doublefault
            item['away_total'] = away_total
            item['away_rec'] = away_rec
            item['away_ser'] = away_ser
            item['away_ser1'] = away_ser1
            item['away_ser2'] = away_ser2
            yield item
        except:
            return []

    def get_percent(self, str):
        startid = str.index('(')+1
        endid = str.index('%')
        sstr = str[startid:endid]
        result = int(sstr, 10)
        return result
    def get_time_from_string(self, str):
        str = str.replace('.', ' ')
        str = str.replace(':', ' ')
        arr = str.split(' ')
        if len(arr) ==  5:
            resultdate = datetime.strptime(str, '%d %m %y %H %M')
        elif len(arr) == 3:
            resultdate = datetime.strptime(str, '%d %m %y')
        else:
            resultdate =datetime.today()
        return resultdate