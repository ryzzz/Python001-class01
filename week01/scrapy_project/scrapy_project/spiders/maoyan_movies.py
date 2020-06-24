# -*- coding: utf-8 -*-
import scrapy


class MaoyanMoviesSpider(scrapy.Spider):
    name = 'maoyan_movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    def parse(self, response):
        pass
