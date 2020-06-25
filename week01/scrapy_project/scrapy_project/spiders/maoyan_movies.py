# -*- coding: utf-8 -*-
import sys
import scrapy
from scrapy.selector import Selector
from scrapy_project.items import ScrapyProjectItem

'''
爬取猫眼top电影信息，存储电影名，电影类型，上映时间到scrapy_project/scrapy_result.csv中
爬取电影数量在settings.py中的MOVIE_NUM修改
'''

class MaoyanMoviesSpider(scrapy.Spider):
    name = 'maoyan_movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/']

    def start_requests(self):
        movie_num = self.settings.get('MOVIE_NUM')
        page_num = (movie_num - 1) // 30 + 1
        for i in range(page_num):
            url = 'https://maoyan.com/films?showType=3&offset={}'.format(i * 30)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        movie_num = self.settings.get('MOVIE_NUM')
        selector_info = Selector(response=response)
        for i, movie_block in enumerate(selector_info.xpath('//div[@class="movie-hover-info"]')):
            if i == movie_num:
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