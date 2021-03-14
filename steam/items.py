# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import Compose, Join, MapCompose, TakeFirst


class SteamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ## test:
    url = scrapy.Field()
    id = scrapy.Field()
    app_name = scrapy.Field()
    price = scrapy.Field()
    reviews = scrapy.Field()


