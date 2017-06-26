# Author DL
from scrapy import cmdline
import os

if os.path.exists('_data/craigslist.json'):
    os.remove('_data/craigslist.json')
else:
    print("No data file exist")

command = "scrapy runspider FatBoySpider.py -o _data/craigslist.json -t json"
cmdline.execute(command.split())