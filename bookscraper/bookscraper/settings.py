# Kích hoạt sipder
ITEM_PIPELINES = {
    'bookscraper.pipelines.MongoPipeline': 300, 
}


SPIDER_MODULES = ['bookscraper.spiders']
NEWSPIDER_MODULE = 'bookscraper.spiders'


# Thông tin kết nối MongoDB
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'books_database'
MONGO_COLLECTION = 'books_collection'

DOWNLOAD_DELAY = 1  
CONCURRENT_REQUESTS = 1