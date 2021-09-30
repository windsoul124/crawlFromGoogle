import scrapy
import pandas as pd
from crawlFromGoogle.items import CrawlfromgoogleItem

class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['']
    # data = pd.read_csv('phone-word.csv')
    data = pd.read_excel('工作簿1.xlsx')

    result = data.values.tolist()
    urls = []
    package = []
    for s in result:
        urls.append('https://www.google.com.pk/search?q=' + s[0])
        package.append(s[0])
    start_urls = urls
    print(package)


    def start_requests(self):
        for i in range(len(self.start_urls)):
            yield scrapy.Request(url=self.start_urls[i],
                                 callback=self.parse,
                                 meta={'data': self.package[i]},
                                 )

    def write_html(self,response):
        with open('1.html', 'wb') as f:
            f.write(response.body)
    def parse(self, response):
        item = CrawlfromgoogleItem()
        item['name'] = response.meta['data']
        # self.write_html(response)
        fields = response.xpath('.//div[@class="ZINbbc xpd O9g5cc uUPGi"]')
        print(fields)


            # print(content_list)