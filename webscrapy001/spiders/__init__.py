import scrapy

class ProductSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        # Extract product details from the listing page
        for product in response.css('.product-list-item'):
            yield {
                'name': product.css('.product-name::text').get(),
                'price': product.css('.product-price::text').get(),
                # Add more fields as needed
            }

        # Follow pagination links
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
