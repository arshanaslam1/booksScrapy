# Books Scraping Project

## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Scraper](#running-the-scraper)
- [Database Schema](#database-schema)
- [Data Validation](#data-validation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project is a Scrapy-based web scraper that extracts book data from [Books to Scrape](http://books.toscrape.com/), validates the data, and stores it in a PostgreSQL database. The scraper captures various details about each book, including title, price, availability, rating, description, and more.

## Project Structure

```
books_scraper/
│
├── books_scraper/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       ├── __init__.py
│       └── books_spider.py
├── scrapy.cfg
└── README.md
```

- `books_scraper/`: Main Scrapy project folder.
- `books_scraper/items.py`: Defines the data structure of items.
- `books_scraper/middlewares.py`: Middleware configurations.
- `books_scraper/pipelines.py`: Data processing and database insertion.
- `books_scraper/settings.py`: Project settings.
- `books_scraper/spiders/`: Contains the spider for scraping the website.
- `scrapy.cfg`: Scrapy configuration file.
- `README.md`: Project documentation.

## Prerequisites

- Python 3.7 or higher
- PostgreSQL
- Scrapy

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/books_scraper.git
    cd books_scraper
    ```

2. **Create a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Install PostgreSQL**:
    Follow the instructions on the [PostgreSQL website](https://www.postgresql.org/download/) to install PostgreSQL on your system.

## Configuration

1. **Database Configuration**:
    Open `books_scraper/settings.py` and set your PostgreSQL connection details:
    ```python
    POSTGRES_HOST = 'localhost'
    POSTGRES_PORT = 5432
    POSTGRES_DB = 'books_db'
    POSTGRES_USER = 'yourusername'
    POSTGRES_PASSWORD = 'yourpassword'
    ```

2. **Create Database and Table**:
    Before running the scraper, ensure you have a PostgreSQL database and table set up. Use the following SQL to create the table:
    ```sql
    CREATE TABLE books (
        id SERIAL PRIMARY KEY,
        title TEXT,
        price TEXT,
        availability TEXT,
        rating TEXT,
        description TEXT,
        upc TEXT,
        product_type TEXT,
        price_excl_tax TEXT,
        price_incl_tax TEXT,
        tax TEXT,
        availability_info TEXT,
        number_of_reviews INTEGER,
        image_url TEXT,
        breadcrumb TEXT[],
        url TEXT,
        slug TEXT
    );
    ```

## Running the Scraper

To run the scraper, execute the following command:
```sh
scrapy crawl books_spider
```

## Database Schema

The table schema for the `books` table in PostgreSQL is as follows:
```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT,
    price TEXT,
    availability TEXT,
    rating TEXT,
    description TEXT,
    upc TEXT,
    product_type TEXT,
    price_excl_tax TEXT,
    price_incl_tax TEXT,
    tax TEXT,
    availability_info TEXT,
    number_of_reviews INTEGER,
    image_url TEXT,
    breadcrumb TEXT[],
    url TEXT,
    slug TEXT
);
```

## Data Validation

The data validation is handled in the `ProductPipeline` class in `books_scraper/pipelines.py`. It includes:

- Removing the `£` symbol and converting the price to float.
- Validating and converting the number of reviews to an integer.
- Removing the `../../` prefix from the image URL.
- Ensuring essential fields like `title`, `price`, and `upc` are present.

If validation fails, the item is dropped.

```python
from scrapy.exceptions import DropItem

class ProductPipeline:
    def process_item(self, item, spider):
        # Validate and clean the 'price' field
        if item.get('price'):
            item['price'] = item['price'].replace('£', '').strip()
            try:
                item['price'] = float(item['price'])
            except ValueError:
                raise DropItem(f"Invalid price: {item['price']}")

        # Validate 'number_of_reviews' field
        if item.get('number_of_reviews'):
            try:
                item['number_of_reviews'] = int(item['number_of_reviews'])
            except ValueError:
                raise DropItem(f"Invalid number of reviews: {item['number_of_reviews']}")

        # Clean 'image_url'
        if item.get('image_url'):
            item['image_url'] = item['image_url'].replace('../../', '')

        # Ensure required fields are not empty
        required_fields = ['title', 'price', 'upc']
        for field in required_fields:
            if not item.get(field):
                raise DropItem(f"Missing {field} in {item}")

        return item
```

## Usage

This project can be used for:
- Scraping book data for analysis or inventory purposes.
- Learning web scraping with Scrapy.
- Building a data pipeline with Scrapy and PostgreSQL.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---