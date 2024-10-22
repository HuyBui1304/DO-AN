import scrapy
import pymongo  
import pandas as pd

class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def __init__(self):
            # Thiết lập kết nối MongoDB
            self.client = pymongo.MongoClient("mongodb://localhost:27017/")  
            self.db = self.client["books_database"] 
            self.collection = self.db["books_collection"]  
            self.data_list = []

    def parse(self, response):
        
            for product_link in response.xpath("//ol[@class='row']/li"):
                try:
                    link = product_link.xpath(".//h3/a/@href").get()
                    full_link = response.urljoin(link)
                except:
                    pass
                yield scrapy.Request(url=full_link, callback=self.parse_name)
            # sang phân trang tiếp theo
            next_page = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_url, callback=self.parse)


    def parse_name(self, response):
        try:
            # Lấy tên sản phẩm
            try:
                product_name = response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get()
            except Exception as e:
                self.log(f"Lỗi khi lấy tên sản phẩm: {e}", level=scrapy.log.ERROR)
                product_name = None

            # Lấy mã sản phẩm
            try:
                product_code = response.xpath("//table[@class='table table-striped']//th[text()='UPC']/following-sibling::td/text()").get()
            except Exception as e:
                self.log(f"Lỗi khi lấy mã sản phẩm: {e}", level=scrapy.log.ERROR)
                product_code = None

            # Lấy loại sản phẩm
            try:
                product_type = response.xpath("//table[@class='table table-striped']//th[text()='Product Type']/following-sibling::td/text()").get()
            except Exception as e:
                self.log(f"Lỗi khi lấy loại sản phẩm: {e}", level=scrapy.log.ERROR)
                product_type = None

            # Lấy giá sản phẩm (chưa có thuế)
            try:
                product_price = response.xpath("//table[@class='table table-striped']//th[text()='Price (excl. tax)']/following-sibling::td/text()").get()
            except Exception as e:
                self.log(f"Lỗi khi lấy giá sản phẩm chưa có thuế: {e}", level=scrapy.log.ERROR)
                product_price = None

            # Lấy giá sản phẩm (đã có thuế)
            try:
                product_price_tax = response.xpath("//table[@class='table table-striped']//th[text()='Price (incl. tax)']/following-sibling::td/text()").get()
            except Exception as e:
                self.log(f"Lỗi khi lấy giá sản phẩm đã có thuế: {e}", level=scrapy.log.ERROR)
                product_price_tax = None

            # Lấy thuế
            try:
                tax = response.xpath("//table[@class='table table-striped']//th[text()='Tax']/following-sibling::td/text()").get()
            except Exception as e:
                self.log(f"Lỗi khi lấy thuế: {e}", level=scrapy.log.ERROR)
                tax = None

            # Lấy tình trạng sẵn có của sản phẩm
            try:
                product_available = response.xpath("//table[@class='table table-striped']//th[text()='Availability']/following-sibling::td/text()").get()
            except Exception as e:
                self.log(f"Lỗi khi lấy tình trạng sẵn có: {e}", level=scrapy.log.ERROR)
                product_available = None

            # Lấy đánh giá sao
            try:
                product_rating = response.xpath("//p[contains(@class, 'star-rating')]/@class").get()
                rating = product_rating.split()[-1]  # Lấy phần cuối cùng của class ('One', 'Two', 'Three', ...)
                star_ratings = {
                    "One": 1,
                    "Two": 2,
                    "Three": 3,
                    "Four": 4,
                    "Five": 5
                }
                stars = star_ratings.get(rating, "Không có đánh giá")
            except Exception as e:
                self.log(f"Lỗi khi lấy đánh giá sao: {e}", level=scrapy.log.ERROR)
                stars = None

            # Lấy đường dẫn hình ảnh sản phẩm
            try:
                image_url = response.xpath("//div[@class='thumbnail']/div[@class='carousel-inner']/div[@class='item active']/img/@src").get()
                image_url = response.urljoin(image_url)  # Chuyển đổi đường dẫn ảnh sang dạng đầy đủ
            except Exception as e:
                self.log(f"Lỗi khi lấy đường dẫn ảnh: {e}", level=scrapy.log.ERROR)
                image_url = None

            # Tạo dữ liệu để chèn vào MongoDB và lưu vào Excel
            product_data = {
                'url': response.url,
                'product_name': product_name,
                'product_code': product_code,
                'product_type': product_type,
                'product_price_excl_tax': product_price,
                'product_price_incl_tax': product_price_tax,
                'tax': tax,
                'product_available': product_available,
                'rating': stars,  # Thêm số sao vào dữ liệu
                'image_url': image_url
            }

            # Chèn dữ liệu vào MongoDB
            self.collection.insert_one(product_data)
            
            # Thêm dữ liệu vào danh sách tạm để xuất ra file Excel
            self.data_list.append(product_data)

        except Exception as e:
            self.log(f"Lỗi khi xử lý dữ liệu sản phẩm: {e}", level=scrapy.log.ERROR)



    def close(self, reason):
            self.client.close()
        
            # Xuất dữ liệu ra file Excel
            df = pd.DataFrame(self.data_list)
            if '_id' in df.columns:
                df = df.drop('_id', axis=1)
            df.to_excel("books_data.xlsx", index=False)
            print('Xuất file thành công')
