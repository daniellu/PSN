# Author DL
from scrapy import cmdline
cmdline.execute("scrapy runspider FatBoySpider.py -o Results/items.json -t json".split())