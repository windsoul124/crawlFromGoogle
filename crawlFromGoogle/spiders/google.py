import scrapy
import pandas as pd
from crawlFromGoogle.items import CrawlfromgoogleItem

class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['']
    data = pd.read_csv('phone-word.csv')
    # data = pd.read_excel('工作簿1.xlsx')

    result = data.values.tolist()
    urls = []
    package = []
    for s in result:
        urls.append('https://www.google.com.pk/search?q=' + s[0])
        package.append(s[0])
    start_urls = urls
    # start_urls = ['https://www.google.com.pk/search?q=OLIVECASH']
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
        fields = response.xpath('.//div[@class="ZINbbc xpd O9g5cc uUPGi"]')
        for i in range(1):
            # 考虑到最开始会有视频 还有一些小标签之类的 要把所有信息提出来 所以分类讨论
            # 所谓的视频标签和正常小块等等的区别 在于标题的class是BNeawe vvjwJb AP7Wnd还是BNeawe deIvCb AP7Wnd
            # 或者有左右的滚轮或者没有左右滚轮（如球队啊视频啊之类的）即len(content_list)是否=2
            #这里结果中会有些一条内容占多行 用str将其拉成一行
            content_list = fields[i].xpath('..//div[@class="BNeawe s3v9rd AP7Wnd"]')
            # if len(content_list) == 2:  # 不是滚轮
            title = fields[i].xpath('..//div[@class="BNeawe vvjwJb AP7Wnd"]/text()').extract_first()
            # if not title:
            #     title = field.xpath('..//div[@class="BNeawe deIvCb AP7Wnd"]//text()').extract_first()
            # 不排除的确是滚轮但是只有两项的情况
            # 不是视频和标签之类 是正常的一个小块
            # if title:
            content = content_list[0].xpath('string(.)').extract_first()
            # url = field.xpath('..//div[@class="BNeawe UPmit AP7Wnd"]/text()').extract_first().replace(' › ', '/')#把>换成/!!!
            url = 'https://www.google.com' + fields[i].xpath('..//a//@href').extract_first().replace(' › ', '/')
            print(content, title, url, '\n')
            item['key'] = response.meta['data']
            item['title'] = title
            item['summary'] = content
            item['url'] = url
            yield item
            #     # 是标签
            #     else:
            #         title = field.xpath('..//div[@class="BNeawe deIvCb AP7Wnd"]/text()').extract_first()
            #         content = content_list[0].xpath('string(.)').extract_first()  # 把�换成/!!!
            #         # url = field.xpath('..//div[@class="BNeawe UPmit AP7Wnd"]/text()').extract_first().replace(' › ', '/')  # 把>换成/!!!
            #         url = 'https://www.google.com'+field.xpath('..//a//@href').extract_first().replace(' › ', '/')
            #         print(str(title), str(content), str(url), '\n')
            #         print('----------------------------------')
            # # 比如republic of china里的Top stories
            # elif len(content_list) == 0:
            #     title = field.xpath('..//div[@class="BNeawe deIvCb AP7Wnd"]//text()').extract_first()
            #     titles = field.xpath('..//div[@class="BNeawe deIvCb AP7Wnd"]//text()').extract()[1:]
            #     content_list = field.xpath('..//a[@class="tHmfQe"]')
            #     for content_ in content_list:
            #         content = content_.xpath('string(..//div[@class="BNeawe deIvCb AP7Wnd"])').extract_first().replace('\n', '')
            #         url = 'https://www.google.com' + content_.xpath('.//@href').extract_first()
            #         print(title, content, url, '\n')
            #         print('----------------------------------')
            # # 在首页的视频里边
            # else:
            #     content_list = field.xpath('..//a[@class="BVG0Nb"]')
            #     title = field.xpath('..//div[@class="BNeawe deIvCb AP7Wnd"]//text()').extract_first()
            #     if not title:
            #         title = field.xpath('..//div[@class="BNeawe vvjwJb AP7Wnd"]/text()').extract_first()
            #     # 不排除title是非首页最上方title的滚轮情况
            #     content_exist = field.xpath('..//div[@class="BNeawe wyrwXc AP7Wnd"]')  # 比如PEOPLE ALSO SEARCH FOR 等标签
            # # 无标签  就正常的最前面的那种大标签
            #     if not content_exist:
            #         for content_ in content_list:
            #             content = content_.xpath('string(.)').extract_first().replace('\n', '')
            #             url = 'https://www.google.com' + content_.xpath('.//@href').extract_first()
            #             print(title, content, url, '\n')
            #             print('----------------------------------')
            # # 有比如PEOPLE ALSO SEARCH FOR / TEAMS 之类标签
            #     else:
            #         block_without_title=field.xpath('..//div[@class="xpc"]')
            #         long_content = ''
            #         iters = block_without_title.xpath('.//div[contains(@class,"jfp3ef")]')
            #         # 决定是内容还是下面的滚轮
            #         key = 0
            #         for iter in iters:
            #             is_label = iter.xpath('./span/div[@class="BNeawe wyrwXc AP7Wnd"]')
            #             if key == 0:
            #                 if not is_label:
            #                     long_content +=iter.xpath('string(.)').extract_first()
            #                 else:
            #                     key = 1
            #                     content=long_content
            #                     url = 'https://www.google.com' + field.xpath('.//@href').extract_first()
            #                     title = iter.xpath('string(.)').extract_first()  # 第一次key=1的title
            #                     print(title, content, url, '\n')
            #                     print('----------------------------------')
            #             else:
            #                 if is_label:
            #                     title = iter.xpath('string(.)').extract_first()
            #                     print(title, content, url, '\n')
            #                     print('----------------------------------')
            #                 else:
            #                     content=iter.xpath('string(.)').extract_first().replace('\n', '')
            #                     url = 'https://www.google.com' + iter.xpath('../../../../a//@href').extract_first()
            #                     print(title, content, url, '\n')
            #                     print('----------------------------------')
