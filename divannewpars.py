import scrapy

class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/sankt-peterburg/category/svet/page-1"]
    total_pages = 7

    def parse(self, response):
        lamps = []
        divans = response.css('div._Ud0k')

        for divan in divans:
            lamp = {
                'name': divan.css('div.lsooF span::text').get(),
                'price': divan.css('div.pY3d2 span::text').get(),
                'url': divan.css('a::attr(href)').get()
            }
            lamps.append(lamp)
            yield lamp

        current_page = int(response.url.split('-')[-1])
        if current_page < self.total_pages:
            next_page = f'https://www.divan.ru/sankt-peterburg/category/svet/page-{current_page + 1}'
            yield scrapy.Request(next_page, callback=self.parse)
