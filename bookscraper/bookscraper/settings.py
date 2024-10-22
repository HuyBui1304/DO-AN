BOT_NAME = "bookscraper"

SPIDER_MODULES = ["bookscraper.spiders"]
NEWSPIDER_MODULE = "bookscraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# MongoDB settings
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'books_database'

# Configure item pipelines
ITEM_PIPELINES = {
    'bookscraper.pipelines.MongoPipeline': 300,
}
# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


DOWNLOAD_DELAY = 0.25
CONCURRENT_REQUESTS_PER_DOMAIN = 1