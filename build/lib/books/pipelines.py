# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import   CsvItemExporter
import pymysql

import logging

class BooksCsvPipeline:
   
    def open_spider(self, spider):
        f = open(f'books.csv', 'wb')
        exporter = CsvItemExporter(f)
        exporter.start_exporting()
        self.exporter = exporter

    def close_spider(self, spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

class BooksMySqlPipeline:
    db_name = 'buyoyo'

    def __init__(self, host,  username, password):
        self.host = host
        self.username = username
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get('MYSQL_HOST')
        username = crawler.settings.get('MYSQL_USERNAME')
        password = crawler.settings.get('MYSQL_PASSWORD')
        return cls(host=host,username = username,password = password)

    def open_spider(self, spider):
        self.id = 0
        self.database = pymysql.connect( host=self.host, port = 3306,database = self.db_name, user = self.username, password = self.password)
        self.cursor = self.database.cursor()
        query = "truncate table books"
        self.cursor.execute(query)
        self.database.commit()

    def close_spider(self, spider):
        if(hasattr(self,'database') and self.database != None):
            self.database.close()

    def process_item(self, item, spider):
        try:
            keys = ",".join(['`{}`'.format(k) for k in item.keys()])
            values = ','.join(['%({})s'.format(k) for k in item.keys()])
            table = "books"
            sql = "insert into {table}({keys}) values({values})".format(table = table,keys=keys,values=values)
            self.cursor.execute(sql, item)
            self.database.commit()
        except Exception as e:
            logging.exception(e)
            self.database.rollback()
        return item