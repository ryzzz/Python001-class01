# -*- coding: utf-8 -*-

# 拉钩网各地区 Python 相关职位 URL
BJ = 'https://www.lagou.com/jobs/list_Python/p-city_2?px=default'
SH = 'https://www.lagou.com/jobs/list_Python/p-city_3?px=default'
GZ = 'https://www.lagou.com/jobs/list_Python/p-city_213?px=default'
SZ = 'https://www.lagou.com/jobs/list_Python/p-city_215?px=default'

# 地区名
REGION_LIST = ['北京', '上海', '广州', '深圳']

# 每个地区爬取职位数量
POSITION_NUM = 100

# 每页职位数量
POSITION_NUM_EACH_PAGE = 15

# mysql 配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'charset': 'utf8mb4'
}
