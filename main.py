# Author DL
import os
import click

from scrapy import cmdline
from FatBoyBot import FatBoyBot


@click.command()
@click.option('--wechat/--no-wechat', default=True, help='Allow wechat integration')
def main(wechat):
    if os.path.exists('_data/craigslist.json'):
        os.remove('_data/craigslist.json')
    else:
        print("No data file exist")

    if wechat:
        FatBoyBot()
    else:
        command = 'scrapy runspider FatBoySpider.py -o _data/craigslist.csv -t csv'
        cmdline.execute(command.split())


if __name__ == '__main__':
    main()