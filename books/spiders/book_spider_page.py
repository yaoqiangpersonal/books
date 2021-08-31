import scrapy
import requests
import time
from lxml import etree
import logging

class BookSpiderPage(scrapy.Spider):
    name = 'book_spider'
    allowed_domains = ['books.com.tw']
    __proxy = "192.168.1.199:7890"
    def start_requests(self):
       for page in range(1,6):
            yield scrapy.Request("https://www.books.com.tw/web/sys_specav/?pb=%E5%82%B3%E8%A8%8A%E6%99%82%E4%BB%A3&md=BD&page=" + str(page),
                                method="GET",
                                headers={
                                            'Accept-Encoding': 'gzip, deflate, br',
                                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                                            'Connection': 'keep-alive',
                                            },
                                meta={"proxy": BookSpiderPage.__proxy},
                                callback=self.parse)

    def parse(self, response):
        if(response.url.find('page') > 0):
            yield from response.follow_all(response.css('.wrap .item>:first-child::attr(href)').getall(), meta={"proxy": BookSpiderPage.__proxy})
        else:
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
                text = requests.get(
                    "https://www.books.com.tw/product_show/getProdCartInfoAjax/"+ id +"/M201105_032_view",
                    headers={"Referer":url},
                    proxies={'http':BookSpiderPage.__proxy,'https':BookSpiderPage.__proxy},
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
