# Author DL
from scrapy import cmdline
import os
from FatBoyBot import FatBoyBot

if os.path.exists('_data/craigslist.json'):
    os.remove('_data/craigslist.json')
else:
    print("No data file exist")

bot = FatBoyBot()
