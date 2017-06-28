from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.contrib.exporter import CsvItemExporter
import os
import csv

class FatBoyPipeline(object):

  def __init__(self):
    self.files = {}
    self.filename = '_data/craigslist.csv'
    self.imported_posts = set()

  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def spider_opened(self, spider):
    includeHeader = not os.path.isfile(self.filename)
    if(not includeHeader):
        self.load_existing_posts(self.filename)

    file = open(self.filename, 'a+b')
    self.files[spider] = file
    self.exporter = CsvItemExporter(file, include_headers_line=includeHeader)
    self.exporter.fields_to_export = ['title', 'post_date', 'price', 'city', 'url']
    self.exporter.start_exporting()

  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    file = self.files.pop(spider)
    file.close()

  def process_item(self, item, spider):
    url = item['url']
    if(url in self.imported_posts):
        raise DropItem("Missing price in %s" % item)
    else:
        self.exporter.export_item(item)
    return item

  def load_existing_posts(self, path):
      with open(path, 'rt') as csvfile:
          reader = csv.DictReader(csvfile)
          for row in reader:
              self.imported_posts.add(row['url'])