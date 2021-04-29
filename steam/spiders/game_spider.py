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
        # Rule(LinkExtractor(allow='page=(\d+)' for full run,
        Rule(LinkExtractor(allow='page=(d+)',
                           restrict_css='.search_pagination_right')
             )
    ]

    def parse_product(self, response):

        price = response.css('.game_purchase_price ::text').extract_first()
        if not price:
            price = response.css('.discount_original_price ::text').extract_first()
        if price:
            price = cleanup(price)

        early_access = response.css('.early_access_header')
        if early_access:
            early_access = True
        else:
            early_access = False

        tags = response.css('a.app_tag ::text').extract()
        clean_tags = []
        for i in tags:
            clean_tags.append(cleanup(i))

        minimum_sys_req = response.css('.game_area_sys_req_leftCol ::text').extract()
        clean_min_sys = []
        for i in minimum_sys_req:
            if cleanup(i) != "":
                clean_min_sys.append(cleanup(i))

        min_processor = ''
        if "Processor:" in clean_min_sys:
            index = clean_min_sys.index("Processor:")
            min_processor = clean_min_sys[index + 1]

        min_mem = ''
        if "Memory:" in clean_min_sys:
            index = clean_min_sys.index("Memory:")
            min_mem = clean_min_sys[index + 1]

        min_gpu = ''
        if "Graphics:" in clean_min_sys:
            index = clean_min_sys.index("Graphics:")
            min_gpu = clean_min_sys[index + 1]

        min_store = ''
        if "Storage:" in clean_min_sys:
            index = clean_min_sys.index("Storage:")
            min_store = clean_min_sys[index + 1]

        minimum_req = [min_processor, min_mem, min_gpu, min_store]

        recommended_sys_req = response.css('.game_area_sys_req_rightCol ::text').extract()
        clean_rec_sys = []
        for i in recommended_sys_req:
            if cleanup(i) != "":
                clean_rec_sys.append(cleanup(i))

        rec_processor = ''
        if "Processor:" in clean_rec_sys:
            index = clean_rec_sys.index("Processor:")
            rec_processor = clean_rec_sys[index + 1]

        rec_mem = ''
        if "Memory:" in clean_rec_sys:
            index = clean_rec_sys.index("Memory:")
            rec_mem = clean_rec_sys[index + 1]

        rec_gpu = ''
        if "Graphics:" in clean_rec_sys:
            index = clean_rec_sys.index("Graphics:")
            rec_gpu = clean_rec_sys[index + 1]

        rec_store = ''
        if "Storage:" in clean_rec_sys:
            index = clean_rec_sys.index("Storage:")
            rec_store = clean_rec_sys[index + 1]

        rec_req = [rec_processor, rec_mem, rec_gpu, rec_store]

        details = response.css('.details_block').extract_first()
        detail = {}
        detail['ea release date'] = 'Nan'
        details = details.split('<br>')

        for line in details:
            line = re.sub('<[^<]+?>', '', line)  # Remove tags.
            line = re.sub('[\r\t\n]', '', line).strip()

            if 'Genre:' in line:
                detail['genre'] = line.replace('Genre: ', '')
            elif 'Developer:' in line:
                detail['developer'] = line.replace('Developer:', '').split('Publisher:')[0]
                detail['publisher'] = re.sub(r'^.*?Publisher:', '', line).split('Release Date:')[0].split('Franchise:')[0]
            elif 'Early Access Release Date' in line:
                detail['ea release date'] = re.sub(r'^.*?Date:', '', line)

        return {
            'id': re.findall('/app/(.*?)/', response.url),
            'url': url_query_cleaner(response.url, ['snr'], remove=True),
            'app_name': response.css('.apphub_AppName ::text').extract_first(),
            'developer': detail['developer'],
            'publisher': detail['publisher'],
            'genre': detail['genre'],
            'tags': clean_tags,
            'price': price,
            'early_access': early_access,
            'early_access_release_date': detail['ea release date'],
            'release_date': response.css('.date ::text').extract(),
            'rating': response.css('.game_review_summary').xpath('../*[@itemprop="description"]/text()').extract(),
            'review_count': response.css('.nonresponsive_hidden').xpath(
                '../*[@itemprop="reviewCount"]/@content').extract(),
            'minimum_sys_req': minimum_req,
            'recommended_sys_req': rec_req,
            'date_scraped': datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
        }
