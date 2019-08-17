import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import os

settings_file_path = 'sports_scrapy.settings' # The path seen from root, ie. from main.py
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())

from time import sleep
sleep(3)
from sports_scrapy.spiders.player_spider import WtaPlayerSpider
process.crawl(WtaPlayerSpider)
process.start() # the script will block here until the crawling is finished