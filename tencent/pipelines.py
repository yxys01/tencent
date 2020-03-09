# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class TencentPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    def open_spider(self, spider):
        '''负责连接数据库'''
        self.db = pymysql.connect()
        # 获取游标对象
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        '''执行数据表的写入操作'''
        # 组装sql语句
        data = dict(item)
        keys = ",".join(data.keys())
        values = ",".join(['%s']*len(data))
        # values为n个%s
        sql = "insert into %s(%s) values(%s)" %(item.table,keys,values)
        # data.values()为列表
        self.cursor.execute(sql,tuple(data.values()))
        self.db.commit()
        return item


    def close_spider(self, spider):
        '''关闭连接数据库'''
        self.db.close()