# -*- coding:utf-8 -*-
#
# Author: Muyang Chen
# Date: 2020-11-22

import re
import time

import requests
from bs4 import BeautifulSoup

import config
from util import PrintLog, HeadersBuilder


class Crawler(object):
    def __init__(self, timeout):
        self.timeout = timeout
        self.headers_builder = HeadersBuilder()

    def _html(self, url):
        headers = self.headers_builder.build()
        try:
            r = requests.get(url, headers=headers, timeout=self.timeout)
            if r.status_code == 200:
                return r.text
        except Exception:
            PrintLog("无法访问：%s，请确保网络畅通后重试！" % url)
            exit(1)

    def _image(self, url):
        headers = self.headers_builder.build()
        try:
            r = requests.get(url, headers=headers, stream=True, timeout=self.timeout)
            if r.status_code == 200:
                return r.content
        except Exception:
            PrintLog("无法访问：%s，请确保网络畅通后重试！" % url)
            exit(1)


class BingCrawler(Crawler):
    def __init__(self, url, timeout):
        Crawler.__init__(self, timeout)
        self.base_url = url
        self.html = self._html(url)
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def image_list(self, page):
        url = "%s?p=%s" % (self.base_url, page)
        html = self._html(url)
        soup = BeautifulSoup(html, 'html.parser')
        image_list = list()
        div_list = soup.find_all('div', class_="card progressive")
        for div in div_list:
            img_page_url = div.find('a').get('href')
            img_html = self._html(self.base_url + img_page_url)
            img_soup = BeautifulSoup(img_html, 'html.parser')
            title = img_soup.find('p', class_="title").get_text()
            title = title.split('(')[0].strip()
            img_url = img_soup.find('img', class_="target progressive__img progressive--not-loaded").get('data-progressive')
            img_url = img_url.split('?')[0].strip()
            image_list.append((title, img_url))

        return image_list

class DownloadImage(Crawler):
    def __init__(self, timeout):
        Crawler.__init__(self, timeout)

    def download(self, url, file_path):
        with open(file_path, 'wb') as f:
            f.write(self._image(url))

if __name__ == '__main__':
    #c = BingCrawler(config.base_url, config.timeout)
    #c.image_list(1)

    di = DownloadImage(config.timeout)
    url = 'http://h2.ioliu.cn/bing/MonfragueNationalPark_ZH-CN5421553314_1920x1080.jpg'
    file_path = r'd:\code\data\image_crawler\test.jpg'
    di.download(url, file_path)
