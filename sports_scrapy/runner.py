import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from sports_scrapy.spiders.player_spider import AtpPlayerSpider

process = CrawlerProcess(get_project_settings())
process.crawl(AtpPlayerSpider)
process.start() # the script will block here until the crawling is finished
