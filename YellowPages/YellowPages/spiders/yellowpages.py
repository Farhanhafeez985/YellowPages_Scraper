import csv

import scrapy
from scrapy import Request


class YellowpagesSpider(scrapy.Spider):
    search_terms = ['wedding reception locations services']
    locations = ['Los Angeles, CA']
    name = 'yellowpages'
    base_url = 'https://www.yellowpages.com'
    allowed_domains = ['yellowpages.com']
    # start_urls = ['https://www.yellowpages.com/']
    for location in locations:
        start_urls = [
            'http://www.yellowpages.com/search?search_terms=wedding+reception+locations+services&geo_location_terms=' + location.replace(
                ',', '%2C').replace(' ', '+') + '']

    custom_settings = {'ROBOTSTXT_OBEY': False, 'LOG_LEVEL': 'INFO',
                       'CONCURRENT_REQUESTS_PER_DOMAIN': 5,
                       'RETRY_TIMES': 5,
                       # 'FEED_URI': 'yp.csv',
                       # 'FEED_FORMAT': 'csv',
                       }

    def parse(self, response):
        # category, business name , phone , email , address, website , detail link
        detail_links = response.xpath("//div[contains(@class,'info-primary')]/h2/a/@href").extract()
        for detail_link in detail_links:
            if not detail_link.startswith(self.base_url):
                detail_link = self.base_url + detail_link
            yield Request(url=detail_link, callback=self.parse_detail)

    def parse_detail(self, response):
        email = str(response.xpath("//a[@class='email-business']/@href").get()).lstrip('mailto:')
        if email:
            business_name = response.xpath("//h1[contains(@class,'business-name')]/text()").get()
            categories = ','.join(response.xpath("//div[@class='categories']/a/text()").extract())
            website = response.xpath("//a[contains(@class,'website-link')]/@href").get()
            phone_number = response.xpath("//a[contains(@class,'phone')]/strong/text()").get()
            street_address = response.xpath("//span[@class='address']/span/text()").get()
            locality = response.xpath("//span[@class='address']/text()").get()
            info = business_name, categories, phone_number, email, street_address + ", " + locality, website, response.request.url
            # fieldnames = ['business name', 'category', 'phone', 'email', 'address', 'website', 'detail link']


    with open('YP_businesses.csv', 'a+', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                # writer.writerow(fieldnames)
                writer.writerow(info)
