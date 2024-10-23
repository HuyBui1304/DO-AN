# Kích hoạt pipeline
ITEM_PIPELINES = {
    'bookscraper.pipelines.MongoPipeline': 300,  # Thay 'my_project' bằng tên thực tế của dự án của bạn
}


SPIDER_MODULES = ['bookscraper.spiders']
NEWSPIDER_MODULE = 'bookscraper.spiders'


# Thông tin kết nối MongoDB
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'books_database'
MONGO_COLLECTION = 'books_collection'