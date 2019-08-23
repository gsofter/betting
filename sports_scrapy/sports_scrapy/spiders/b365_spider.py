import scrapy
import re
from  datetime import datetime
from urllib.parse import urljoin
import time
from time import sleep
import random

class AtpBetSpider(scrapy.Spider):
    pipelines = ['atpbet']
    name = 'atpbet'
    custom_settings = {
        'FEED_URI' : name + datetime.today().strftime("_%Y%m%d.csv"),
        'FEED_FORMAT' : 'csv',
    }
    
    proxy_pool =  ["51.68.172.7:3128", 
                    "176.123.61.238:3128",
                    '111.231.140.109:8888',
                ]

    def start_requests(self):
        url  =  "https://www.bet365.com/#/AC/B13/C1/D50/E2/F163/"
        meta = {
            'proxy' : "51.68.172.7:3128",
        }
        req = scrapy.Request(url=url, callback=self.parse, meta=meta)
        yield req

    def parse(self, response):
        html_file = open("bet365.html", "w")
        html_file.write(response.body.decode('utf-8'))
        
        matches = response.xpath('.//div[contains(@class, "gll-MarketGroupContainer")]')
        yield {
            'url' : response.url,
        }
