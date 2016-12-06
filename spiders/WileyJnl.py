import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from EdgeCrawler.items import ArticleItem

# class WileyJnlSpider (scrapy.Spider):
# 	name = "WileyJnl"
# 	urls = [
# 		'http://onlinelibrary.wiley.com/browse/publications?type=journal'
# 	]

class WileyJnlSpider (scrapy.Spider):
	name = "WileyJnl"
	start_urls = [
		'http://onlinelibrary.wiley.com/doi/10.1002/mrm.24178/full'
	]

	def parse (self, response):
		l = ItemLoader (item=ArticleItem(), response=response)
		l.default_output_processor = TakeFirst()
		l.replace_css ('doi',      'span.article-header__meta-info-data::text')
		l.replace_css ('year',     'time.article-header__meta-info-data::attr(datetime)')
		l.replace_css ('authors',  'h3.article-header__authors-name::text')
		l.replace_css ('cited_by', 'a.article-section__citation-link::attr(href)')
		l.replace_css ('title',    'h1.article-header__title::text')
		l.replace_css ('abstract', 'div.mainAbstract p::text')
		yield l.load_item()

		# Follow next page in the issue
		next_page = response.css ("a.issue-header__arrow--right::attr(href)").extract_first()
		if next_page is not None:
			yield scrapy.Request (next_page, callback=self.parse)

		# # Follow citation links
		# next_pages = article.css ("a.article-section__citation-link::attr(href)").extract()
		# for next_page in next_pages:
		# 	yield scrapy.Request (next_page, callback=self.parse)
