import scrapy
import requests
import time

import logging
from books.daos import BooksDao

import xlrd
from lxml import etree

class BookSpiderXls(scrapy.Spider):
    name = 'book_spider_xls'
    allowed_domains = ['books.com.tw']
    __proxy = "192.168.1.199:7890"
    def start_requests(self):
        path = "C:/Users/SomeOne/Desktop/urls.xls"
        data = xlrd.open_workbook(path)
        table = data.sheet_by_index(0)
        nrows = table.nrows

        for i in range(1,nrows):
            yield scrapy.Request(table.row_values(i)[1],
                                meta={"proxy":BookSpiderXls.__proxy},
                                callback=self.parse
                                )
       

    def parse(self, response):
        main = response.css('.grid_10')
        name = main.css('.mod h1::text').get()
        no = main.css('.type02_p003 li').re_first(r'產品編號：([a-zA-Z0-9-]+)')
        company = main.css('.type02_p003 li').re_first(r'發行公司：(?:<a.+?>)?(\w+)(?:</a>)?')
        price = main.css('.price01 b::text').get()
        url = response.url
        if(url.find('?') > 0):
            id = url[url.rfind("/")+1:url.rfind("?")]
        else:
            id = url[url.rfind("/")+1:len(url)]

        stock = ""
        text = ""
        try:
            time.sleep(3)
            text = requests.get(
                "https://www.books.com.tw/product_show/getProdCartInfoAjax/"+ id +"/M201105_032_view",
                headers={"Referer":url},
                proxies={'http':BookSpiderXls.__proxy,'https':BookSpiderXls.__proxy},
                timeout=5
                ).text
            if(text.strip() != ""):
                content = etree.HTML(text)
                stock = content.xpath("//li[@class='no']/text()")[0] 
                if(stock.find('存')> 0):
                    stock = stock + content.xpath("//li[@class='no']/strong/text()")[0]

        except Exception as e:
            logging.exception(e)
            logging.error(text)
        yield {
            'id':id,
            'name':name,
            'no':no,
            'price':price,
            'stock':stock,
            'company':company
        }
