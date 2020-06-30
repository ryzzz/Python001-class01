# -*- coding: utf-8 -*-

import os
import pandas as pd
from scrapy.exceptions import NotConfigured


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyProjectPipeline(object):
    def __init__(self):
        self.movie_info_list = []

    def process_item(self, item, spider):
        if not spider.settings.get('MOVIE_NUM'):
            raise NotConfigured
        self.movie_num = spider.settings.get('MOVIE_NUM')
        self.movie_info_list.append(item)
        if len(self.movie_info_list) == self.movie_num:
            df = pd.DataFrame(self.movie_info_list)
            df.to_csv('./scrapy_result.csv', index=False)
            return item
