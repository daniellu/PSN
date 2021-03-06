# Author DL

import scrapy
from datetime import datetime, timedelta
from post_item import PostItem
import re
import GitHubPublisher
from system_config import system_config


class FatBoySpider(scrapy.Spider):
    name = 'fatboy-spider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'FatBoyPipeline.FatBoyPipeline': 300
        }
    }

    start_urls = (list(map(lambda x: x['url'], system_config['cities_data_sources'])))
    current_year = datetime.today().year
    end_time = datetime.now() - timedelta(days=7)
    keywords = ['cash buyer', 'owner financ', 'investment', 'rehab',
                        'private fund', 'note that owner financing', 'owner financed','owner financ']
    should_stop = {}

    def __init__(self):
        for url in self.start_urls:
            self.should_stop[self.getDomainUrl(url)] = False

    def parse(self, response):
        domain_url = self.getDomainUrl(response.url)
        for result_info in response.css('p.result-info'):
            result_time = result_info.css('time ::text').extract_first()
            title = result_info.css('a.result-title ::text').extract_first()
            detail_link = self.getDomainUrl(response.url) + result_info.css('a.result-title::attr(href)').extract_first()

            result_time_object = self.parseDateTime(result_time + ' ' + str(self.current_year))
            yield scrapy.Request(detail_link, callback=self.parseDetail)
            #if the current item is older than the last n days
            #the crawler can stop at this item
            if (result_time_object < self.end_time):
                temp = self.should_stop[domain_url]
                self.should_stop[domain_url] = True
                break


        if False == self.should_stop[domain_url]:
            next_page_url = response.css('a.next::attr(href)').extract_first()
            if next_page_url is not None:
                yield response.follow(self.getDomainUrl(response.url) + next_page_url, self.parse)

    def closed(self, reason):
        print('Fat boy crawler finished')
        today = datetime.today().strftime('%B-%d-%Y')
        filename = system_config['export_file_name']
        publisher = GitHubPublisher.GitHubPublisher(system_config['github_token'], system_config['github_repo'])
        publisher.publish(filename)


    def parseDetail(self, response):
        item = PostItem()
        item['url'] = response.url
        item['title'] = response.css('span[id=titletextonly] ::text').extract_first()
        item['post_date'] = response.css('time ::text').extract_first()
        item['price'] = response.css('span.price ::text').extract_first()
        detail = response.css('section[id=postingbody] ::text').extract()
        # here we need to do some regex matching to decide if the post need to be yielp
        if self.decideIfPostContainKeyWords(detail):
            yield item

    def parseDateTime(self, date_string):
        datetime_object = datetime.strptime(date_string, '%b %d %Y')
        return datetime_object

    def decideIfPostContainKeyWords(self, detail):
        detail = str(detail)
        for word in self.keywords:
            matches = re.search(word, detail)
            if matches is not None:
                return True
        return False

    def getDomainUrl(self, url):
        return url[:url.index('/search')]


