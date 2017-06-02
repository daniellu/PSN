# Author DL

import scrapy
from datetime import datetime, timedelta
from scrapy import Item
from post_item import PostItem
import re


class FatBoySpider(scrapy.Spider):
    name = 'fatboy-spider'
    domain_url = 'https://kansascity.craigslist.org'
    start_urls = ['https://kansascity.craigslist.org/search/rea']
    should_stop = False
    current_year = datetime.today().year
    end_time = datetime.now() - timedelta(days=7)
    content_to_match = ['cash buyer', 'owner financ', 'investment', 'rehab',
                        'private fund', 'note that owner financing', 'owner financed','owner financ']

    def parse(self, response):
        for result_info in response.css('p.result-info'):
            result_time = result_info.css('time ::text').extract_first()
            title = result_info.css('a.result-title ::text').extract_first()
            detail_link = self.domain_url + result_info.css('a.result-title::attr(href)').extract_first()

            result_time_object = self.parseDateTime(result_time + ' ' + str(self.current_year))
            if (result_time_object < self.end_time):
                self.should_stop = True

            yield scrapy.Request(detail_link, callback=self.parseDetail)

        if False == self.should_stop:
            for next_page in response.css('span.buttons.next > a'):
                yield response.follow(next_page, self.parse)

    def parseDetail(self, response):
        item = PostItem()
        item['url'] = response.url
        item['title'] = response.css('span[id=titletextonly] ::text').extract_first()
        item['post_date'] = response.css('time ::text').extract_first()
        item['price'] = response.css('span.price ::text').extract_first()
        item['detail'] = response.css('section[id=postingbody] ::text').extract()
        # here we need to do some regex matching to decide if the post need to be yielp
        if self.decideIfPostContainKeyWords(item):
            yield item

    def parseDateTime(self, date_string):
        datetime_object = datetime.strptime(date_string, '%b %d %Y')
        return datetime_object

    def decideIfPostContainKeyWords(self, item):
        detail = str(item['detail'])
        matches = re.search('owner financ', detail)
        if matches is not None:
            return True
        return False
