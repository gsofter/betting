import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import os

settings_file_path = 'sports_scrapy.settings' # The path seen from root, ie. from main.py
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process1 = CrawlerProcess(get_project_settings())
process2 = CrawlerProcess(get_project_settings())


from time import sleep
sleep(3)
from sports_scrapy.spiders.matches_spider import AtpMatchSpider
# from sports_scrapy.spiders.perform_spider import AtpPerformSpider
# from sports_scrapy.spiders.odd_spider import AtpOddSpider

from sports_scrapy.spiders.matches_spider import WtaMatchSpider
# from sports_scrapy.spiders.perform_spider import WtaPerformSpider
# from sports_scrapy.spiders.odd_spider import WtaOddSpider

process1.crawl(AtpMatchSpider )
process2.crawl(WtaMatchSpider )

process1.start() # the script will block here until the crawling is finished
# process2.start() # the script will block here until the crawling is finished
# process3.start() # the script will block here until the crawling is finished
# process4.start() # the script will block here until the crawling is finished
# process5.start() # the script will block here until the crawling is finished
# process6.start() # the script will block here until the crawling is finished