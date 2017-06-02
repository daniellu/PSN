# Author DL

import scrapy
from scrapy import Field

class PostItem(scrapy.Item):
    url = Field()
    title = Field()
    detail = Field()
    post_date = Field()
    price = Field()