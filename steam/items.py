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
    id = scrapy.Field()
    url = scrapy.Field()
    app_name = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    early_access = scrapy.Field()
    release_date = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    minimum_sys_req = scrapy.Field()
    recommended_sys_req = scrapy.Field()
    date_scraped = scrapy.Field()


