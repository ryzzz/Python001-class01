# -*- coding: utf-8 -*-

import json
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

'''
爬取拉钩北上广深 Python 工程师薪资
'''
# ----------------------------
# 拉钩网各地区 Python 相关职位 URL
BJ = 'https://www.lagou.com/jobs/list_Python/p-city_2?px=default'
SH = 'https://www.lagou.com/jobs/list_Python/p-city_3?px=default'
GZ = 'https://www.lagou.com/jobs/list_Python/p-city_213?px=default'
SZ = 'https://www.lagou.com/jobs/list_Python/p-city_215?px=default'

# 爬取职位数量
POSITION_NUM = 16

# 延迟
DOWNLOAD_DELAY = 3
# ----------------------------
ua = UserAgent(verify_ssl=False)
user_agent = ua.random
header = {'User-Agent': user_agent, 'origin': 'https://www.lagou.com',
          'referer': 'https://www.lagou.com/jobs/list_Python'}


def start_requests(region):
    # 获取session
    session = requests.Session()
    session.get(url='https://www.lagou.com/jobs/list_python', headers=header, timeout=3)
    
    page_num = (POSITION_NUM - 1) // 15 + 1
    for i in range(page_num):
        page = i + 1
        data = {'first': True, 'pn': page, 'kd': 'python'}
        response = session.post(
            url='https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(region),
            data=data, headers=header)
        print('Status code: {}'.format(response.status_code))
        #print('URL: ' + response.url)
        #print(response.text)
        time.sleep(DOWNLOAD_DELAY)
        parse(response, page)

def parse(response, page):
    remaining_position_num = POSITION_NUM - (page - 1) * 15

    #todo: 解析页面
    selector_info = Selector(response=response)
    try:
        for i, movie_block in enumerate(selector_info.xpath('//div[@class="movie-hover-info"]')):
            if i == remaining_position_num:
                break
            movie_name = None
            movie_type = None
            movie_time = None
            item = ScrapyProjectItem()
            for movie_info in movie_block.xpath('./div'):
                movie_name = movie_info.xpath('./@title').extract_first()
                div_text = movie_info.xpath('./text()').extract()
                span_text = movie_info.xpath('./span/text()').extract_first()
                if span_text == '类型:':
                    movie_type = div_text[1].strip()
                elif span_text == '上映时间:':
                    movie_time = div_text[1].strip()
            item['movie_name'] = movie_name
            item['movie_type'] = movie_type
            item['movie_time'] = movie_time
            yield item
    except Exception as e:
        print(e)
    

def oldspider(region_url):
    header = {'User-Agent': user_agent, 'Cookie': COOKIE}
    response = requests.get(url=region_url, headers=header)
    print('URL: ' + response.url)
    print('Status code: {}'.format(response.status_code))

    bs_info = bs(response.text, 'html.parser')
    result_list = []

    for i, movie_block in enumerate(bs_info.find_all('div', attrs={'class': 'movie-hover-info'})):
        if i == POSITION_NUM:
            break
        movie_name = None
        movie_type = None
        movie_time = None
        for movie_info in movie_block.find_all('div'):
            movie_name = movie_info.get('title')
            span = movie_info.find('span')
            if span.text == '类型:':
                movie_type = movie_info.text.split()[-1]
            elif span.text == '上映时间:':
                movie_time = movie_info.text.split()[-1]
        result = {'movie_name': movie_name, 'movie_type': movie_type, 'movie_time': movie_time}
        result_list.append(result)

    df = pd.DataFrame(result_list)
    df.to_csv('./requests_bs4_result.csv', index=False)
    print('Done')


if __name__ == '__main__':
    start_requests('广州')
