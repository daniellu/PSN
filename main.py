# Author DL
from scrapy import cmdline
import os
#from FatBoyBot import FatBoyBot
from FatBoySpider import FatBoySpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

if os.path.exists('_data/craigslist.json'):
    os.remove('_data/craigslist.json')
else:
    print("No data file exist")

#bot = FatBoyBot()

setting = get_project_settings()
setting['ITEM_PIPELINES'] = {
    'FatBoyPipeline.FatBoyPipeline': 300,
}
process = CrawlerProcess(setting)
process.crawl(FatBoySpider)
process.start()  # the script will block here until the crawling is finished