# -*- coding: utf-8 -*-

import re
import scrapy

from bs4 import BeautifulSoup
from ..items import AppsItem


class Apps(scrapy.Spider):
    name = 'apps'
    start_urls = [
        'http://zhushou.360.cn/list/index/cid/1?page=',
        'http://zhushou.360.cn/list/index/cid/2?page=',
    ]
    allowed_domains = ['zhushou.360.cn']

    def start_requests(self):
        for starturl in self.start_urls:
            for pageNum in range(1, 51):
                url = starturl + str(pageNum)
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        app_url = re.findall(r'<li><a sid=.*?href="(.*?)">', response.text)
        for url in app_url:
            yield scrapy.Request('http://zhushou.360.cn' + url, callback=self.parse_item)

    def parse_item(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        item = AppsItem()
        item['name'] = soup.find_all(id='app-name')[0].span.get_text()
        item['url'] = 'http://10.3.200.200:9999/' + soup.select('a[class^="js-downLog dbtn"]')[0]['href'].split('url=http://')[1]
        virus = soup.find_all('li', 'item-1')[0]
        item['virus'] = virus.get_text()
        item['ad'] = virus.next_sibling.next_sibling.get_text()
        return item
