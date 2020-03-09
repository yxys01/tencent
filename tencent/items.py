# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HrItem(scrapy.Item):
    # define the fields for your item here like:
    table = "hr" # 表名
    id = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    type = scrapy.Field()
    number = scrapy.Field()
    duty = scrapy.Field()
    requirement = scrapy.Field()

