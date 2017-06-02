# Author DL

import scrapy
from scrapy import Field

class PostItem(scrapy.Item):
    title = Field()
    detail = Field()
    post_date = Field()
    price = Field()