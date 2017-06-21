# Author DL
from scrapy import cmdline
command = "scrapy runspider FatBoySpider.py -o _data/craigslist.json -t json"
cmdline.execute(command.split())