# -*- coding: utf-8 -*-
import scrapy
from tencent.items import HrItem

class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?keywords=python&lid=2156']

    def parse(self, response):
        # 解析当前招聘信息的url地址
        detail_urls = response.css('tr.even a::attr(href), tr.odd aa::attr(href)')
        # 遍历
        for url in detail_urls:
            # 完整的地址
            fullurl = response.urljoin(url)
            # print(fullurl)
            # 获取该url下一页的详细信息
            yield scrapy.Request(url=fullurl,callback=self.parse_page)

        # 获取下一页的url地址
        next_url = response.css('#next::attr(href)').extract_first()
        if next_url != 'javascript:;':
            url = response.urljion(next_url)
            yield scrapy.Request(url=url,callback=self.parse)

    def parse_page(self,response):
        '''解析招聘详情信息'''
        hr = HrItem()
        hr['id'] = response.selector.re_first('onclick="applyPosition\(([0-9]+)\);"')
        hr['title'] = response.css('#sharetitle::text').extract_first() #id
        hr['location'] = response.selector.re_first('<span class="lightblue 12">工作地点：</span>(.*?)</td>')
        hr['type'] = response.selector.re_first('<span class="lightblue">职位类别：</span>(.*?)</td>')
        hr['number'] = response.selector.re_first('<span class="lightblue">招聘人数：</span>([0-9]+)人</td>')

        duty = response.xpath("//table//tr[3]//li//text()").extract()
        hr['duty'] = " ".join(duty)

        requirement = response.xpath("//table//tr[4]//li//text()").extract()
        hr['requirement'] = " ".join(requirement)

        # 交给管道文件
        yield hr