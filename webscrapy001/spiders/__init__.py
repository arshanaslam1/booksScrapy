import scrapy

from webscrapy001.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        # Extract product details from the listing page

        for product in response.css('article.product_pod div.image_container a::attr(href)').getall():
            yield response.follow(product, self.parse_product)

        # Follow pagination links
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        # Extract product details from the product page
        item = ProductItem()
        item['title'] = response.css('article.product_page h1::text').get()
        item['price'] = response.css('p.price_color::text').get()
        item['availability'] = response.css('p.availability::text').get().strip()
        item['rating'] = response.css('p.star-rating::attr(class)').re_first(r'star-rating (\w+)')
        item['description'] = response.css('#product_description + p::text').get()
        item['upc'] = response.css('table.table-striped th:contains("UPC") + td::text').get()
        item['product_type'] = response.css('table.table-striped th:contains("Product Type") + td::text').get()
        item['price_excl_tax'] = response.css('table.table-striped th:contains("Price (excl. tax)") + td::text').get()
        item['price_incl_tax'] = response.css('table.table-striped th:contains("Price (incl. tax)") + td::text').get()
        item['tax'] = response.css('table.table-striped th:contains("Tax") + td::text').get()
        item['availability_info'] = response.css('table.table-striped th:contains("Availability") + td::text').get()
        item['number_of_reviews'] = response.css('table.table-striped th:contains("Number of reviews") + td::text').get()
        item['image_url'] = response.css("div.item img::attr(src)").get()
        item['breadcrumb'] = response.css('ul.breadcrumb a::text').getall()
        item['url'] = response.url
        item['slug'] = response.url.split('/')[-2]
        yield item
