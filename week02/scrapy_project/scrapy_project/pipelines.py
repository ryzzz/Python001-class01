# -*- coding: utf-8 -*-

#import pandas as pd
import pymysql
from scrapy.exceptions import NotConfigured


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyProjectPipeline(object):

    # 存储到 mysql 数据库中
    # 开启爬虫时执行，只执行一次
    def open_spider(self, spider):
        if not spider.settings.get('MYSQL_CONFIG'):
            raise NotConfigured
        mysql_config = spider.settings.get('MYSQL_CONFIG')
        # 创建连接
        self.conn = pymysql.connect(
            host=mysql_config['host'],
            port=mysql_config['port'],
            user=mysql_config['user'],
            password=mysql_config['password'],
            charset=mysql_config['charset']
        )
        # 创建游标
        self.cur = self.conn.cursor()
        # 创建库如果库不存在
        self.cur.execute("create database if not exists maoyan")
        # 使用库
        self.cur.execute("use maoyan")
        # 创建表如果表不存在
        self.cur.execute("create table if not exists top(movie_name text, movie_time text, movie_type text)")

    def process_item(self, item, spider):
        try:
            self.cur.execute("insert into top(movie_name, movie_time, movie_type) values ('{}', '{}', '{}');".format(item['movie_name'], item['movie_time'], item['movie_type']))
            # 插入成功提交事务
            self.conn.commit()
        except Exception as e:
            # 插入失败回退
            print('写入数据失败')
            print(e)
            self.conn.rollback()
        return item

    # 关闭爬虫时执行，只执行一次
    def close_spider(self, spider):
        # 关闭游标
        self.cur.close()
        # 关闭连接
        self.conn.close()

    # # 存储到 csv 文件中
    # # 开启爬虫时执行，只执行一次
    # def open_spider(self, spider):
    #     self.movie_info_list = []
    #
    # def process_item(self, item, spider):
    #     self.movie_info_list.append(item)
    #     return item
    #
    # # 关闭爬虫时执行，只执行一次
    # def close_spider(self, spider):
    #     df = pd.DataFrame(self.movie_info_list)
    #     df.to_csv('./scrapy_result.csv', index=False)
