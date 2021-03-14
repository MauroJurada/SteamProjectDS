import scrapy
import pandas as pd

import re

from w3lib.url import canonicalize_url, url_query_cleaner

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class game_spider(CrawlSpider):
    name = "games"
    allowed_domains =['steampowered.com']
    # Adapt with Tags to limit crawling ie: 'https://store.steampowered.com/search/?sort_by=Released_DESC&tags=492' for tag Indie (or &vrsupport=401 for VR only)
    start_urls = ['https://store.steampowered.com/search/?sort_by=Released_DESC&tags=492']

    rules = [
        #Every steam game page follows this rule: https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/
        Rule(LinkExtractor(allow='/app/(.+)/',
                           restrict_css='#search_result_container'),
             callback='parse_item'),
        Rule(LinkExtractor(allow='page=(d+)',
                           restrict_css='.search_pagination_right')
             )
    ]

    def parse_product(self, response):
        return {
            'app_name': response.css('.apphub_AppName ::text').extract_first()
        }