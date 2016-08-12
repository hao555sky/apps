# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy

from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from sqlalchemy.orm import sessionmaker
from .models import Apps, db_connect, create_apps_table

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/52.0.2743.116 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'keep-alive',
    'Referer': 'http://www.yougetsignal.com/tools/web-sites-on-web-server/',
    'X-Requested-With': 'XMLHttpRequest'
}


class MyFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['url'])

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        item['file_paths'] = file_paths[0]
        return item


class AppsPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_apps_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        app = Apps(**item)

        try:
            session.add(app)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
