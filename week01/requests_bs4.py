# -*- coding=utf-8 -*-

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

'''
爬取猫眼top10电影信息
使用requests获取页面内容
使用BeautifulSoup解析页面内容
使用pandas将解析结果保存在同目录下csv文件中
'''
#----------------------------
# 猫眼电影top页面链接
URL = 'https://maoyan.com/films?showType=3'
# 代理
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
# 猫眼电影首次进入会跳转美团验证页面，在浏览器中验证后将cookie复制到这里
COOKIE = 'uuid_n_v=v1; uuid=C9DC78C0B5EC11EAA1F189776DB49E05E5738CACDADE4974A02CC499DA916529; _csrf=d8595a669bf88499438c27cfee9ced7f638222b687994aebc831323b6b0bb79a; _lxsdk_cuid=172e53d9e8b48-03f090d8d3be3d-4353760-240000-172e53d9e8cc8; _lxsdk=C9DC78C0B5EC11EAA1F189776DB49E05E5738CACDADE4974A02CC499DA916529; mojo-uuid=3d3033e3315c555f41796e8c3e5607ab; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1592983920,1592983939,1592984076; mojo-session-id={"id":"9f05796af0806090a150b4f96d7c567a","time":1592986323738}; mojo-trace-id=9; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1592988094; __mta=213163691.1592983920571.1592988077505.1592988094254.13; _lxsdk_s=172e53d9e8d-6c3-852-7a8%7C%7C36'
# 爬取电影数量，上限30个
MOVIE_NUM = 10
#----------------------------

header = {'User-Agent': USER_AGENT, 'Cookie': COOKIE}
response = requests.get(url=URL, headers=header)
print('URL: ' + response.url)
print('Status code: {}'.format(response.status_code))

bs_info = bs(response.text, 'html.parser')
result_list = []

for i, movie_block in enumerate(bs_info.find_all('div', attrs={'class': 'movie-hover-info'})):
    if i == MOVIE_NUM:
        break
    movie_name = None
    movie_type = None
    movie_time = None
    for movie_info in movie_block.find_all('div', attrs={'class': 'movie-hover-title'}):
        movie_name = movie_info.get('title')
        span = movie_info.find('span')
        if span.text == '类型:':
            movie_type = movie_info.text.split()[-1]
        elif span.text == '上映时间:':
            movie_time = movie_info.text.split()[-1]
    result = {'name':movie_name, 'type': movie_type, 'time': movie_time}
    result_list.append(result)

df = pd.DataFrame(result_list, columns=['name', 'type', 'time'])
df.to_csv('./request_bs4_result.csv', index=False)
print('Done')