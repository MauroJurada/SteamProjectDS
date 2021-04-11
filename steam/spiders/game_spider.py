import scrapy
import pandas as pd
import re
from w3lib.url import canonicalize_url, url_query_cleaner
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime

def cleanup(response):
    return response.replace("\t", "").replace("\r", "").replace("\n", "").replace("\u20ac", "")


class game_spider(CrawlSpider):
    name = "games"
    allowed_domains = ['steampowered.com']
    # Adapt with Tags to limit crawling ie: 'https://store.steampowered.com/search/?sort_by=Released_DESC&tags=492' for tag Indie (or &vrsupport=401 for VR only)
    start_urls = ['https://store.steampowered.com/search/?sort_by=Released_DESC&tags=492']

    rules = [
        # Every steam game page follows this rule: https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/
        Rule(LinkExtractor(allow='/app/(.+)/',
                           restrict_css='#search_result_container'),
             callback='parse_product'),
        Rule(LinkExtractor(allow='page=(d+)',
                           restrict_css='.search_pagination_right')
             )
    ]

    def parse_product(self, response):
        price = cleanup(response.css('.game_purchase_price ::text').extract_first())
        if not price:
            price = cleanup(response.css('.discount_original_price ::text').extract_first())


        early_access = response.css('.early_access_header')
        if early_access:
            early_access = True
        else:
            early_access = False

        tags = response.css('a.app_tag ::text').extract()
        clean_tags = []
        for i in tags:
            clean_tags.append(cleanup(i))

        minimum_sys_req = response.css('.game_area_sys_req_leftCol').extract()
        recommended_sys_req = response.css('.game_area_sys_req_rightCol').extract()

        return {
            'id': re.findall('/app/(.*?)/', response.url),
            'url': url_query_cleaner(response.url, ['snr'], remove=True),
            'app_name': response.css('.apphub_AppName ::text').extract_first(),
            # 'specs': response.css('.game_area_details_specs a ::text').extract(),
            'tags': clean_tags,
            'price': price,
            'early_access': early_access,
            'release_date': response.css('.date ::text').extract(),
            'rating': response.css('.game_review_summary').xpath('../*[@itemprop="description"]/text()').extract(),
            'review_count': response.css('.nonresponsive_hidden').xpath('../*[@itemprop="reviewCount"]/@content').extract(),
            'minimum_sys_req': minimum_sys_req,
            'recommended_sys_req': recommended_sys_req,
            'date_scraped': datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
        }
