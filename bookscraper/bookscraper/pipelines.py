import pymongo
import pandas as pd

class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.data_list = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION')
        )


    def open_spider(self, spider):
        # Thiết lập kết nối MongoDB
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]


    def process_item(self, item, spider):
        # Chèn dữ liệu vào MongoDB và thêm vào danh sách tạm để xuất Excel
        self.collection.insert_one(dict(item))  # Lưu vào MongoDB
        self.data_list.append(dict(item))  # Thêm dữ liệu vào danh sách tạm
        return item





    def close_spider(self, spider):
        self.client.close()
        # Xuất dữ liệu ra file Excel
        
        df = pd.DataFrame(self.data_list)
        if '_id' in df.columns:
            df = df.drop('_id', axis=1)
        df.to_excel("books_data.xlsx", index=False)


