# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlfromgoogleItem(scrapy.Item):
    title = scrapy.Field()
    name = scrapy.Field()
    pass
