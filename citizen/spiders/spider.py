import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import CitizenItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class CitizenSpider(scrapy.Spider):
	name = 'citizen'
	start_urls = ['https://www.citizens-bank.com/news/']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//span[@class="fl-post-info-date"]/text()').get()
		title = response.xpath('//h1/span/text()').get()
		content = response.xpath('//div[@class="fl-module fl-module-fl-post-content fl-node-599c6b46b54ad"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=CitizenItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
