import scrapy


class BookSpiderSpider(scrapy.Spider):
    name = 'book_spider'
    allowed_domains = ['books.com.tw']
    proxy = "192.168.1.199:7890"
    def start_requests(self):
       for page in range(1,27):
            yield scrapy.Request("https://www.books.com.tw/web/sys_specav/?o=1&v=2&f=Y&md=BD&page=" + str(page),
                                method="GET",
                                headers={
                                         
                                            'Accept-Encoding': 'gzip, deflate, br',
                                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                                            'Connection': 'keep-alive',
                                            },
                                meta={"proxy": self.proxy},
                                callback=self.parse)

    def parse(self, response):
        if(response.url.find('page') > 0):
            yield from response.follow_all(response.css('.wrap .item>:first-child::attr(href)').getall(), meta={"proxy": self.proxy})
        else:
            main = response.css('.grid_10')
            name = main.css('.mod h1::text').get()
            attr = main.css('.type02_p003 li').getall()
            price = main.css('.price01 b::text').get()
            url = response.url
            id = url[url.rfind("/")+1:url.rfind("?")-1]
            yield {
                'id':id,
                'name':name,
                'attr':attr,
                'price':price
            }
