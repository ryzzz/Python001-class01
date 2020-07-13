# -*- coding: utf-8 -*-


import time
import random
import pymysql
import requests
import pandas as pd
from fake_useragent import UserAgent
from multiprocessing import Process, Queue
from multiprocessing.dummy import Pool as ThreadPool

try:
    from config import *
except:
    from week03.LagouSpider.config import *

'''
爬取拉钩北上广深 Python 工程师薪资
'''

ua = UserAgent(verify_ssl=False)
user_agent = ua.random

header = {'User-Agent': user_agent, 'origin': 'https://www.lagou.com',
          'referer': 'https://www.lagou.com/jobs/list_Python'}

# 获取session
session = requests.Session()
session.get(url='https://www.lagou.com/jobs/list_python', headers=header, timeout=3)

result_queue = Queue(100)

page_num = (POSITION_NUM - 1) // POSITION_NUM_EACH_PAGE + 1


def run_spider():
    store_proc = StoreToMySQL(result_queue)
    store_proc.start()
    pool = ThreadPool(len(REGION_LIST))
    pool.map(each_region, REGION_LIST)
    pool.close()
    pool.join()
    result_queue.put('Done')
    store_proc.join()
    print('Finish.')


def each_region(region):
    pool = ThreadPool(page_num)
    for page in range(1, page_num + 1):
        pool.apply_async(each_page, (page, region))
    pool.close()
    pool.join()


def each_page(page, region):
    time.sleep(random.random() * 3)
    data = {'first': True, 'pn': page, 'kd': 'python'}
    response = session.post(
        url='https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(region),
        data=data, headers=header)
    # print(region)
    # print('Status code: {}'.format(response.status_code))
    # print('URL: ' + response.url)
    # print(response.text)
    parse(response, page, region)


def parse(response, page, region):
    remaining_position_num = POSITION_NUM - (page - 1) * POSITION_NUM_EACH_PAGE
    info = response.json()
    result_list = info['content']['positionResult']['result']
    for i, result in enumerate(result_list):
        if i == remaining_position_num:
            break
        pos_name = result['positionName']
        money = result['salary']
        result_queue.put((region, pos_name, money))
        print(region, pos_name, money)

class StoreToMySQL(Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def conn_mysql(self):
        self.conn = pymysql.connect(
            host=MYSQL_CONFIG['host'],
            port=MYSQL_CONFIG['port'],
            user=MYSQL_CONFIG['user'],
            password=MYSQL_CONFIG['password'],
            charset=MYSQL_CONFIG['charset']
        )
        self.cur = self.conn.cursor()
        self.cur.execute("create database if not exists lagou")
        self.cur.execute("use lagou")
        self.cur.execute("create table if not exists python(region text, position text, money text)")

    def run(self):
        self.conn_mysql()
        while True:
            if not self.queue.empty():
                try:
                    region, pos_name, money = self.queue.get()
                except:
                    break
                try:
                    self.cur.execute(
                        "insert into python(region, position, money) values ('{}', '{}', '{}');".format(region, pos_name, money))
                    self.conn.commit()
                except Exception as e:
                    print(e)
                    self.conn.rollback()
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    run_spider()
