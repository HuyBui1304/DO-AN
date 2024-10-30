import scrapy
import re

class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for product_link in response.xpath("//ol[@class='row']/li"):
            try:
                link = product_link.xpath(".//h3/a/@href").get()
                full_link = response.urljoin(link)
                yield scrapy.Request(url=full_link, callback=self.parse_name)
            except:
                pass

        # sang phân trang tiếp theo
        next_page = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
    # chuẩn hoá dữ liệu sang dạng double và int
    def normalize_data(self, value, data_type):
        try:
            if data_type == "double" and value:
                return float(value.replace('£', '').strip())
            elif data_type == "int" and value:
                return int(re.search(r'\d+', value).group())
        except:
            return None

    def parse_name(self, response):
        try:
            # Lấy dữ liệu sản phẩm
            try:
                product_name = response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get()
            except:
                product_name = ''

            try:
                product_code = response.xpath("//table[@class='table table-striped']//th[text()='UPC']/following-sibling::td/text()").get()
            except:
                product_code = ''

            try:
                book_type = response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()
            except:
                book_type = ''

            try:
                product_price = response.xpath("//table[@class='table table-striped']//th[text()='Price (excl. tax)']/following-sibling::td/text()").get()
                product_price = self.normalize_data(product_price, data_type="double")
            except:
                product_price = ''

            try:
                product_price_tax = response.xpath("//table[@class='table table-striped']//th[text()='Price (incl. tax)']/following-sibling::td/text()").get()
                product_price_tax = self.normalize_data(product_price_tax, data_type="double")
            except:
                product_price_tax = ''

            try:
                tax = response.xpath("//table[@class='table table-striped']//th[text()='Tax']/following-sibling::td/text()").get()
                tax = self.normalize_data(tax, data_type="double")
            except:
                tax = ''

            try:
                product_available = response.xpath("//table[@class='table table-striped']//th[text()='Availability']/following-sibling::td/text()").get()
                product_available = self.normalize_data(product_available, data_type="int")
            except:
                product_available = ''
            
            try:
                # Lấy thông tin đánh giá sao của sản phẩm
                rating_class = response.xpath("//p[contains(@class, 'star-rating')]/@class").get()
                rating_text = rating_class.split()[-1]  
                star_ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
                stars = star_ratings.get(rating_text, None)  
            except:
                stars = None

            try:
                image_url = response.xpath("//div[@class='thumbnail']/div[@class='carousel-inner']/div[@class='item active']/img/@src").get()
                image_url = response.urljoin(image_url)
            except:
                image_url = ''

            # Tạo dữ liệu sản phẩm
            product_data = {
                'url': response.url,
                'product_name': product_name,
                'product_code': product_code,
                'book_type': book_type,
                'product_price_excl_tax': product_price,
                'product_price_incl_tax': product_price_tax,
                'tax': tax,
                'product_available': product_available,
                'rating': stars,
                'image_url': image_url
            }

            # Trả về dữ liệu để pipeline xử lý
            yield product_data

        except:
            pass


        