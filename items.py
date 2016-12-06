# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Identity, MapCompose


# class EdgeCrawlerItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class ArticleItem (scrapy.Item):

	#---------------------------------
	# Filters

	# Extracts year from date string
	def filter_year (datestr):
		for s in datestr.split ('-'):
			if s.isdigit(): return s

	# Strips commas and spaces
	def filter_strip (s):
		return s.strip (', ');

	#---------------------------------
	# Item fields

	doi = scrapy.Field()

	year = scrapy.Field	(
		input_processor  = MapCompose (filter_year),
	)

	authors = scrapy.Field	(
		input_processor  = MapCompose (filter_strip),
		output_processor = Identity(),
	)

	cited_by = scrapy.Field	(
		output_processor = Identity(),
	)

	title    = scrapy.Field()
	abstract = scrapy.Field()
