# -*- coding: utf-8 -*-

import pandas as pd
import pymysql
from scrapy.exceptions import NotConfigured


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyProjectPipeline(object):

    # 可选择写入MYSQL或CSV
    # 开启爬虫时执行，只执行一次
    def open_spider(self, spider):
        if not spider.settings.get('DATA_STORE'):
            raise NotConfigured
        self.data_store = spider.settings.get('DATA_STORE')
        self.init_mysql(spider) if self.data_store == 'mysql' else self.init_csv_list()

    def process_item(self, item, spider):
        self.insert_mysql(item) if self.data_store == 'mysql' else self.append_csv_list(item)
        return item

    # 关闭爬虫时执行，只执行一次
    def close_spider(self, spider):
        self.disconnect_mysql() if self.data_store == 'mysql' else self.write_csv()

    # 连接mysql并创建库和表
    def init_mysql(self, spider):
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

    # mysql插入数据
    def insert_mysql(self, item):
        try:
            self.cur.execute("insert into top(movie_name, movie_time, movie_type) values ('{}', '{}', '{}');".format(
                item['movie_name'], item['movie_time'], item['movie_type']))
            # 插入成功提交事务
            self.conn.commit()
        except Exception as e:
            # 插入失败回退
            print('写入数据失败')
            print(e)
            self.conn.rollback()

    # 断开mysql
    def disconnect_mysql(self):
        # 关闭游标
        self.cur.close()
        # 关闭连接
        self.conn.close()

    # 创建列表
    def init_csv_list(self):
        self.movie_info_list = []

    # 列表添加数据
    def append_csv_list(self, item):
        self.movie_info_list.append(item)

    # 将列表数据入csv
    def write_csv(self):
        df = pd.DataFrame(self.movie_info_list)
        df.to_csv('./scrapy_result.csv', index=False)
