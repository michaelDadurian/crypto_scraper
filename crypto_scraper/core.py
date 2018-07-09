from spiders.cmc_spider import CMCSpider
from spiders.prices_spider import PricesSpider

from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess, Crawler

from scrapy.settings import Settings


TO_CRAWL = [CMCSpider, PricesSpider]
RUNNING_CRAWLERS = []

def spider_closing(spider):
    """Activates on spider closed signal"""
    log.info("Spider closed: %s" % spider, level=log.INFO)
    RUNNING_CRAWLERS.remove(spider)
    if not RUNNING_CRAWLERS:
        reactor.stop()
		
#log.start(loglevel=log.DEBUG)
for spider in TO_CRAWL:
  
    crawler = Crawler(spider())
    crawler_obj = spider(spider)
    RUNNING_CRAWLERS.append(crawler_obj)

    # stop reactor when spider closes
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)

    crawler.crawl(crawler)
  

# blocks process so always keep as the last statement
reactor.run()


