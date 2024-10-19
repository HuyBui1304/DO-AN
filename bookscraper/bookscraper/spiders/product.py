import scrapy
import pymongo  # Thư viện để kết nối MongoDB

class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def __init__(self):
        # Thiết lập kết nối MongoDB
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")  # Thay đổi URL nếu MongoDB của bạn chạy ở nơi khác
        self.db = self.client["books_database"]  # Tên database bạn muốn sử dụng
        self.collection = self.db["books_collection"]  # Tên collection

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
        image_url = response.xpath("//div[@class='thumbnail']//img/@src").get()
        image_url = response.urljoin(image_url) # Chuyển đổi đường dẫn ảnh sang dạng đầy đủ

        # Tạo dữ liệu để chèn vào MongoDB
        product_data = {
            'url': response.url,
            'product_name': product_name,
            'product_code': product_code,
            'product_type': product_type,
            'product_price_excl_tax': product_price,
            'product_price_incl_tax': product_price_tax,
            'tax': tax,
            'product_available': product_available
        }

        # Chèn dữ liệu vào MongoDB
        self.collection.insert_one(product_data)

    def close(self, reason):
        # Đóng kết nối MongoDB khi spider hoàn tất
        self.client.close()