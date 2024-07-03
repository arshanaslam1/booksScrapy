# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from scrapy.exceptions import DropItem


class BookItemValidationPipeline:
    def process_item(self, item, spider):
        if not item.get("slug", None):
            raise DropItem("Missing slug in %s" % item)
        item["slug"] = item["slug"].replace("-", "_")
        item["image_url"] = item["image_url"].replace("../..", "http://books.toscrape.com")
        return item


class PostgresPipeline:
    def __init__(self, hostname, username, password, database, port, batch_size):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.batch_size = batch_size
        self.connection = None
        self.cursor = None
        self.items_buffer = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            hostname=crawler.settings.get("POSTGRES_HOST", "localhost"),
            username=crawler.settings.get("POSTGRES_USERNAME", "books"),
            password=crawler.settings.get("POSTGRES_PASSWORD", "books"),
            database=crawler.settings.get("POSTGRES_DATABASE", "to_books"),
            port=crawler.settings.get("POSTGRES_PORT", 5400),
            batch_size=crawler.settings.get("POSTGRES_BATCH_SIZE", 500),
        )

    def open_spider(self, spider):
        self.connection = psycopg2.connect(host=self.hostname, user=self.username, password=self.password,
                                           dbname=self.database, port=self.port)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        if self.items_buffer:
            self._commit_items()
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        if self._find_record_by_slug(item.get('slug')) is not None:
            raise DropItem(f"Duplicate item found: {item}")
        self.items_buffer.append(item)
        if len(self.items_buffer) >= self.batch_size:
            self._commit_items()
        return item

    def _commit_items(self):
        insert_query = """
        INSERT INTO books (
            title,
            price,
            availability,
            rating,
            description,
            upc,
            product_type,
            price_excl_tax,
            price_incl_tax,
            tax,
            availability_info,
            number_of_reviews,
            image_url,
            breadcrumb,
            url,
            slug
            ) VALUES (
                   %(title)s,
                    %(price)s,
                    %(availability)s,
                    %(rating)s,
                    %(description)s,
                    %(upc)s,
                    %(product_type)s,
                    %(price_excl_tax)s,
                    %(price_incl_tax)s,
                    %(tax)s,
                    %(availability_info)s,
                    %(number_of_reviews)s,
                    %(image_url)s,
                    %(breadcrumb)s,
                    %(url)s,
                    %(slug)s
            );
        """
        self.cursor.executemany(insert_query, self.items_buffer)
        self.connection.commit()
        self.items_buffer = []

    def _find_record_by_slug(self, slug_value):
        record = next((record for record in self.items_buffer if record.get('slug') == slug_value), None)
        return record