import scrapy
import pymongo
import pandas as pd  # Thư viện để xuất dữ liệu sang Excel

class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def __init__(self):
        # Thiết lập kết nối MongoDB
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["books_database"]
        self.collection = self.db["books_collection"]

        # Tạo một danh sách để lưu trữ dữ liệu thu thập được
        self.products_data = []

    def parse(self, response):
        for product_link in response.xpath("//ol[@class='row']/li"):
            link = product_link.xpath(".//h3/a/@href").get()
            full_link = response.urljoin(link)
            yield scrapy.Request(url=full_link, callback=self.parse_name)

        next_page = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_name(self, response):
        product_name = response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get()
        product_code = response.xpath("//table[@class='table table-striped']//th[text()='UPC']/following-sibling::td/text()").get()
        product_type = response.xpath("//table[@class='table table-striped']//th[text()='Product Type']/following-sibling::td/text()").get()
        product_price = response.xpath("//table[@class='table table-striped']//th[text()='Price (excl. tax)']/following-sibling::td/text()").get()
        product_price_tax = response.xpath("//table[@class='table table-striped']//th[text()='Price (incl. tax)']/following-sibling::td/text()").get()
        tax = response.xpath("//table[@class='table table-striped']//th[text()='Tax']/following-sibling::td/text()").get()
        product_available = response.xpath("//table[@class='table table-striped']//th[text()='Availability']/following-sibling::td/text()").get()

        # Lấy đường dẫn hình ảnh sản phẩm
        image_url = response.xpath("//div[@class='thumbnail']/div[@class='carousel-inner']/div[@class='item active']/img/@src").get()
        image_url = response.urljoin(image_url)  # Chuyển đổi đường dẫn ảnh sang dạng đầy đủ

        # Tạo dữ liệu để chèn vào MongoDB và lưu trữ trong danh sách
        product_data = {
            'url': response.url,
            'product_name': product_name,
            'product_code': product_code,
            'product_type': product_type,
            'product_price_excl_tax': product_price,
            'product_price_incl_tax': product_price_tax,
            'tax': tax,
            'product_available': product_available,
            'image_url': image_url
        }

        # Chèn dữ liệu vào MongoDB
        self.collection.insert_one(product_data)

        # Thêm dữ liệu vào danh sách
        self.products_data.append(product_data)

    def close(self, reason):
        # Đóng kết nối MongoDB khi spider hoàn tất
        self.client.close()

        # Chuyển dữ liệu từ danh sách sang DataFrame
        df = pd.DataFrame(self.products_data)

        # Lưu DataFrame vào file Excel
        df.to_excel("books_data.xlsx", index=False)  # Chuyển dữ liệu sang file Excel

        self.log("Dữ liệu đã được lưu vào file Excel thành công!")
