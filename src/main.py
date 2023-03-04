# -*- coding:utf-8 -*-
#
# Author: Muyang Chen
# Date: 2021-07-10

import os
from util import PrintLog
import time
import random

import config
from crawler import BingCrawler

if __name__ == '__main__':
    base_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.path.pardir))
    output_dir = base_path.replace('python', 'data')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_dir = os.path.join(output_dir, 'image_list.txt')
    url_set = set()
    cur_id = 0
    with open(output_dir, 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.strip().split('\t')
            if len(fields) < 3:
                continue

            _id = int(fields[0])
            url = fields[2]
            url_set.add(url)
            if cur_id < _id:
                cur_id = _id

    with open(output_dir, 'a+', encoding='utf-8') as f:
        c = BingCrawler(config.base_url, config.timeout)
        for i in range(100):
            page = i + 1
            PrintLog("Start to get page: %s" % page)
            image_list = c.image_list(i)
            for title, url in image_list:
                if url in url_set:
                    continue

                cur_id += 1
                _output = '%s\t%s\t%s\n' % (cur_id, title, url)
                f.write(_output)
                f.flush()
                print("Save: %s" % _output)
                if not cur_id % 5:
                    sleep_time = random.randint(120, 600)
                    PrintLog("cur_id: %s, sleep %ss." % (cur_id, sleep_time))
                    time.sleep(sleep_time)
