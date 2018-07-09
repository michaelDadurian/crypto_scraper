import scrapy
import re
import mysql.connector
#import spider_config
from datetime import datetime
import time

import signal

def handler(signum, frame):
    print ('Got CTRL+C')
    exit (0)

signal.signal(signal.SIGINT, handler)

coin = input("Enter coin, replaces spaces with '-': ").lower()
print(coin)



coin_lookup = {
	"bitcoin" : "BTC",
	"ethereum": "ETH",
	"vechain" : "VEN",
	"stellar" : "XLM",
	"tron"    : "TRX",
	"litecoin": "LTC"
}

"""
try:
	connection = mysql.connector.connect(
						user='mdadurian',
						password='Wafflefries12@', 
						host='127.0.0.1', 
						database='crypto_scraper')
						
	if connection.is_connected():
		print('Connected to crypto database')
		
except Error as e:
	print(e)

cursor = connection.cursor()
sql = ""CREATE TABLE IF NOT EXISTS Coin (NAME CHAR(5) NOT NULL, USD FLOAT, VOLUME LONG, DATE DATETIME())""
cursor.execute(sql)
connection.close()
"""
class CMCSpider(scrapy.Spider):
	name = "cmc"
	

	#Returns an iterable of Requests which the Spider begins to crawl from
	def start_requests(self):
		
		
		urls = [
			
			'https://coinmarketcap.com/',
			'https://prices.org/'
			
			
		]
		#'https://prices.org/'
		#'https://coincheckup.com/',
		#'https://www.livecoinwatch.com/'
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse, errback=self.errback_httpbin)
			
	#Handles the response downloaded from each request
	def parse(self, response):
		
		signal.signal(signal.SIGINT, handler)
		
		self.logger.info('Got successful response from %s' % response.url)
		self.logger.info('STATUS: %d' % response.status)
		
		if 'prices' in response.url:
			code = coin_lookup[coin]
			print(code)
			xpath_usd_str = '//*[@id="' + code + '"]/td[3]' 
			xpath_vol_str = '//*[@id="' + code + '"]/td[8]'
			site = "prices.org"
		else:
			xpath_usd_str = '//*[@id="id-' + coin + '"]/td[4]/a'
			xpath_vol_str = '//*[@id="id-' + coin + '"]/td[5]/a'
			site = "coinmarketcap.com"

		"""Begin parsing"""
		most_recent_price = 0
		data_file = coin + ".txt"
		
		
		try:
			fr = open(data_file, 'r')
			lines = fr.readlines()
			most_recent_price = lines[-1].split(' ')[0]
			print(most_recent_price)
			
		except IOError:
			fr = open(data_file, 'w')
		
		fr.close()
		
		curr_usd = re.findall('"([^"]*)"', response.xpath(xpath_usd_str).re(r'data-usd.*')[0])[0]
		curr_vol = re.findall('"([^"]*)"', response.xpath(xpath_vol_str).re(r'data-usd.*')[0])[0]
		#print (int(float(curr_vol)))
		curr_time = datetime.now()
		curr_time = curr_time.strftime('%Y-%m-%d %H:%M:%S')
		
		
		"""Write data to file"""
		
		line = curr_usd + ' ' + curr_vol + ' ' + curr_time + ' ' + site + '\n'
		print(line)
		
		with open (data_file, 'a') as fw:
			if (float(most_recent_price) != float(curr_usd)): 
				fw.write(line)
					
					
		fw.close()
		
		#time.sleep(1)
		yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
		"""
		try:
			cursor.execute("INSERT INTO bitcoin (date, usd, volume) VALUES ('%s', %d, %d)", (time.strftime('%Y-%m-%d %H:%M:%S'), curr_usd, curr_vol))
			connection.commit()
		except:
			connection.rollback()
		"""	

		
			
			
		
		
	def errback_httpbin(self, failure):
		# log all failures
		self.logger.error(repr(failure))

		# in case you want to do something special for some errors,
		# you may need the failure's type:

		if failure.check(HttpError):
			# these exceptions come from HttpError spider middleware
			# you can get the non-200 response
			response = failure.value.response
			self.logger.error('HttpError on %s', response.url)

		elif failure.check(DNSLookupError):
			# this is the original request
			request = failure.request
			self.logger.error('DNSLookupError on %s', request.url)

		elif failure.check(TimeoutError, TCPTimedOutError):
			request = failure.request
			self.logger.error('TimeoutError on %s', request.url)
			
			

		
	
		