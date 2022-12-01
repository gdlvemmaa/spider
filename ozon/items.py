# Define here the models for your scraped items
import scrapy


class OzonItem(scrapy.Item):
    name = scrapy.Field()
    os_version = scrapy.Field()
