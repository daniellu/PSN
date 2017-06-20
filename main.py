# Author DL
from scrapy import cmdline
from datetime import datetime, timedelta

today = datetime.today().strftime('%B-%d-%Y')
command = "scrapy runspider FatBoySpider.py -o Results/" + today + ".json -t json"
cmdline.execute(command.split())