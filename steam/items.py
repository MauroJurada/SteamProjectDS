# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, Join, MapCompose, TakeFirst


class SteamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ## test:
    id = scrapy.Field()
    app_name = scrapy.Field()
    pass

class GamesItemLoader(ItemLoader):
    default_output_processor = Compose(TakeFirst())
