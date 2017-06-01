# Author DL

import scrapy
from datetime import datetime, timedelta

class FatBoySpider(scrapy.Spider):
    name = 'fatboy-spider'
    start_urls = ['https://kansascity.craigslist.org/search/rea']
    should_stop = False
    current_year = datetime.today().year
    end_time = datetime.now() - timedelta(days=2)

    def parse(self, response):
        for result_info in response.css('p.result-info'):
            result_time = result_info.css('time ::text').extract_first()
            title = result_info.css('a.result-title ::text').extract_first()
            yield {'date': result_time, 'title': title}

            result_time_object = self.parseDateTime(result_time + ' ' + str(self.current_year))
            if(result_time_object < self.end_time):
                self.should_stop = True

        if(self.should_stop == False):
            for next_page in response.css('span.buttons.next > a'):
                yield response.follow(next_page, self.parse)

    def parseDateTime(self, date_string):
        datetime_object = datetime.strptime(date_string, '%b %d %Y')
        return datetime_object