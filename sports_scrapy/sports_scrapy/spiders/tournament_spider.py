import scrapy
import re
from sports_scrapy.items import AtpMatchItem
from time import sleep
import time
from  datetime import datetime

class AtpTournamentSpider(scrapy.Spider):
    pipelines = ['atptournament']
    name = 'atptournament'
    start_urls = [
        'https://www.xscores.com/tennis/tournaments/atp-tour/2019',
    ]

    def parse(self, response):
        tour_rows = response.xpath('.//div[contains(@class, "score_row tennis_row")]')
        for tour_row in tour_rows:
            date_str = tour_row.xpath('./div[1]/text()').extract_first().strip()
            date = datetime.strptime(date_str, '%d-%m-%Y').date()
            
            name = tour_row.xpath('./div[2]/text()').extract_first().strip()

            location = tour_row.xpath('./div[3]/text()').extract_first().strip()

            series = tour_row.xpath('./div[5]/text()').extract_first().strip()
            surface = tour_row.xpath('./div[6]/text()').extract_first().strip()
            price = tour_row.xpath('./div[7]/text()').extract_first().strip()
            round_str = tour_row.xpath('./div[8]/text()').extract_first().strip()
            round = ''
            try: 
                _id = round_str.index('-')
                round = round_str[:_id]
            except:
                round = round_str
            yield {
                'round' : round,
                'date' : date,
                'name' : name,
                'location' : location,
                'series' : series,
                'surface' : surface,
                'price' : price
            }
        return []

