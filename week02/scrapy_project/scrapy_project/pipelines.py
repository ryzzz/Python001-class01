# -*- coding: utf-8 -*-

import os
import pandas as pd


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyProjectPipeline(object):
    def process_item(self, item, spider):
        df = pd.DataFrame(dict(item), index=[0])
        if os.path.exists('./scrapy_result.csv'):
            header = False
        else:
            header = True
        df.to_csv('./scrapy_result.csv', mode='a', index=False, header=header)
        return item
