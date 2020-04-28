# -*- coding: utf-8 -*-
import scrapy


class ScrapeSpringerBooksSpider(scrapy.Spider):
    name = 'scrape_springer_books'
    allowed_domains = ['towardsdatascience.com/', 'link.springer.com']
    start_urls = ['https://towardsdatascience.com/springer-has-released-65-machine-learning-and-data-books-for-free-961f8181f189/']

    def __init__(self, *args, **kwargs):    
        super(scrapy.Spider, self).__init__(*args, **kwargs)


    def parse(self, response):
        # Select all links related to link.springer domain
        links = response.xpath('//a[contains(@href, "link.springer")]/@href')
        for link in links:
            yield scrapy.Request(link.get(), callback=self.gotospringer)

    def gotospringer(self, response):
        link = 'https://' + self.allowed_domains[1] +   response.xpath('//a[contains(@data-track-action, "pdf")]/@href')[0].get()
        file_name = response.xpath('//h1/text()').get() if response.xpath('//h1/text()').get() else ''
        yield scrapy.Request(link, callback=self.save_pdf, meta={'file_name': file_name})

    def save_pdf(self, response):
        path = response.meta.get('file_name').replace(' ', '_').lower()+'.pdf' if response.meta.get('file_name') else response.url.split('/')[-1]
        with open(path, 'wb') as f:
            f.write(response.body)
        