from django.core.management.base import BaseCommand
from sports_scrapy.sports_scrapy.spiders.player_spider import AtpPlayerSpider 
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl(AtpPlayerSpider)
process.start()
