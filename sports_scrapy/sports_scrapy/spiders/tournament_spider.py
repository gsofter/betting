import scrapy
import re
from sports_scrapy.items import AtpTournamentItem
from sports_scrapy.items import WtaTournamentItem
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
            try: 
                item = AtpTournamentItem()
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
                
                item['round'] = round
                item['date'] = date
                item['name'] =name
                item['location'] = location
                item['series'] = series
                item['surface'] = surface
                item['price'] = price
                yield item
            except:
                print('Confirm the element is existing')
                pass


class WtaTournamentSpider(scrapy.Spider):
    pipelines = ['wtatournament']
    name = 'wtatournament'
    start_urls = [
        'https://www.xscores.com/tennis/tournaments/wta-tour/2019',
    ]

    def parse(self, response):
        tour_rows = response.xpath('.//div[contains(@class, "score_row tennis_row")]')
        for tour_row in tour_rows:
            try: 
                item = WtaTournamentItem()
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
                
                item['round'] = round
                item['date'] = date
                item['name'] =name
                item['location'] = location
                item['series'] = series
                item['surface'] = surface
                item['price'] = price
                yield item
            except:
                print('Confirm the element is existing')
                pass
