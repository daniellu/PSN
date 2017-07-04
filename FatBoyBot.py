# Author DL
from FatBoySpider import FatBoySpider
from scrapy.crawler import CrawlerProcess
from scrapy import cmdline
import itchat, time
from itchat.content import *
from scrapy.utils.project import get_project_settings
import subprocess

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
            subprocess.call("scrapy runspider FatBoySpider.py -o _data/craigslist.csv -t csv", shell=True)
            return 'Go to https://daniellu.github.io/FBL/ to view the results'
        else:
            return FatBoyBot.bullshit_reply(message)

    @staticmethod
    def bullshit_reply(message):
        return 'Fuck you'