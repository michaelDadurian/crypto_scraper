from spiders.cmc_spider import CMCSpider
from spiders.prices_spider import PricesSpider

from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess, Crawler

from scrapy.settings import Settings
import signal
from multiprocessing import Process, Queue


TO_CRAWL = [CMCSpider, PricesSpider]
RUNNING_CRAWLERS = []

"""
def spider_closing(spider):
    #Activates on spider closed signal
    log.info("Spider closed: %s" % spider, level=log.INFO)
    RUNNING_CRAWLERS.remove(spider)
    if not RUNNING_CRAWLERS:
		reactor.stop()

"""

def handler(signum, frame):
    print ('Got CTRL+C')
    exit (0)

def run_spider(spider):
	def setup(queue):
		try:
			runner = crawler.CrawlerRunner()
			deferred = runner.crawl(spider)
			deferred.addBoth(lambda _: reactor.stop())
			reactor.run()
			queue.put(None)
		except:
			queue.put(e)
	queue = Queue()
	p = Process(target=setup, args=(queue,))
	p.start()
	result = queue.get()
	p.join()
	
	if result is not None:
		raise result
	

#log.start(loglevel=log.DEBUG)
for spider in TO_CRAWL:
	
	signal.signal(signal.SIGINT, handler)
	run_spider(spider)
	
	"""
	print(spider.name)
	process = CrawlerProcess({'USER_AGENT': 'Michael Dadurian github.com/michaelDadurian'})
	process.crawl(spider)
	process.start()
	"""

# blocks process so always keep as the last statement


