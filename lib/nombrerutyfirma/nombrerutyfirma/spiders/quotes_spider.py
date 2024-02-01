# scrapy crawl quotes -o ../../output/nombrerutyfirma.json
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.nombrerutyfirma.com/rut?term=7.140.723-3',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        """

    def parse(self, response):
        for quote in response.xpath('/html/body/div[2]/div/table'):
            yield {
                'nombre': quote.xpath('/html/body/div[2]/div/table/tbody/tr/td[1]/text()').extract_first(),
                'run': quote.xpath('/html/body/div[2]/div/table/tbody/tr/td[2]/text()').extract_first(),
                'direccion': quote.xpath('/html/body/div[2]/div/table/tbody/tr/td[4]/text()').extract_first(),
                'ciudad/comuna': quote.xpath('/html/body/div[2]/div/table/tbody/tr/td[5]/text()').extract_first(),
            }