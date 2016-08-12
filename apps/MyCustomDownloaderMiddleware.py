# -*- coding: utf-8 -*-

import scrapy
import subprocess


class MyCustomDownloader(object):

    def process_request(self, request, spider):
        if request.url.endswith(".apk"):
            subprocess.Popen(["wget", request.url])
            return scrapy.http.HtmlResponse(url='', body='', encoding='utf-8')