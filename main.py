# Author DL
from scrapy import cmdline
import os
from FatBoyBot import FatBoyBot
from FatBoySpider import FatBoySpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

if os.path.exists('_data/craigslist.json'):
    os.remove('_data/craigslist.json')
else:
    print("No data file exist")

bot = FatBoyBot()

#command = "scrapy runspider FatBoySpider.py -o _data/craigslist.csv -t csv"
#cmdline.execute(command.split())
