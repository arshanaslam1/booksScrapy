# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Webscrapy001Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
    description = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability_info = scrapy.Field()
    number_of_reviews = scrapy.Field()
    image_url = scrapy.Field()
    breadcrumb = scrapy.Field()
    url = scrapy.Field()
    slug = scrapy.Field()