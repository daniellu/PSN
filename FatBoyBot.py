# Author DL
from FatBoySpider import FatBoySpider
from scrapy.crawler import CrawlerProcess
import itchat, time
from itchat.content import *
from scrapy.utils.project import get_project_settings

class FatBoyBot(object):
    def __init__(self):
        itchat.auto_login(True)
        itchat.run()

    @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
    def text_reply(msg):
        message_text = msg['Text']
        reply_text = FatBoyBot.process_message(message_text, msg['FromUserName'])
        itchat.send('%s: %s' % (msg['Type'], reply_text), msg['FromUserName'])

    @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
    def download_files(msg):
        msg['Text'](msg['FileName'])
        return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

    @itchat.msg_register(TEXT, isGroupChat=True)
    def text_reply(msg):
        if msg['isAt']:
            itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])

    @staticmethod
    def process_message(message, receiver):
        if('干活' in str(message)):
            return FatBoyBot.run_scraper(None, None, None, receiver)
        else:
            return FatBoyBot.bullshit_reply(message)

    @staticmethod
    def bullshit_reply(message):
        return 'Fuck you'

    @staticmethod
    def run_scraper(source, start_date, end_date, receiver):
        setting = get_project_settings()
        setting['ITEM_PIPELINES'] = {
            'FatBoyPipeline.FatBoyPipeline': 300,
        }
        process = CrawlerProcess(setting)
        process.crawl(FatBoySpider)
        process.start()  # the script will block here until the crawling is finished

        return 'Go to https://daniellu.github.io/FBL/ to view the results'