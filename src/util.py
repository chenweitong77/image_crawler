# -*- coding:utf-8 -*-
#
# Author: Muyang Chen
# Date: 2021-07-10

import datetime
import random

import config


# 打印日志函数
def PrintLog(log_str):
    time_ = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[%s] %s' % (time_, log_str))


# 创建请求Headers
# Usage:
# headers_builder = HeadersBuilder()
# headers = headers_builder.build()
class HeadersBuilder(object):
    def __init__(self):
        self.user_agents = config.user_agents

    def build(self):
        headers = dict()
        idx = random.randint(0, len(self.user_agents) - 1)
        headers['User-Agent'] = self.user_agents[idx]
        return headers
