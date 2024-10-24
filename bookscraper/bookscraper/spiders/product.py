import scrapy

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

    def parse_name(self, response):
        try:
            # Lấy dữ liệu sản phẩm
            try:
                product_name = response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get()
            except:
                pass

            try:
                product_code = response.xpath("//table[@class='table table-striped']//th[text()='UPC']/following-sibling::td/text()").get()
            except:
                pass

            try:
                product_type = response.xpath("//table[@class='table table-striped']//th[text()='Product Type']/following-sibling::td/text()").get()
            except:
                pass

            try:
                product_price = response.xpath("//table[@class='table table-striped']//th[text()='Price (excl. tax)']/following-sibling::td/text()").get()
            except:
                pass

            try:
                product_price_tax = response.xpath("//table[@class='table table-striped']//th[text()='Price (incl. tax)']/following-sibling::td/text()").get()
            except:
                pass

            try:
                tax = response.xpath("//table[@class='table table-striped']//th[text()='Tax']/following-sibling::td/text()").get()
            except:
                pass

            try:
                product_available = response.xpath("//table[@class='table table-striped']//th[text()='Availability']/following-sibling::td/text()").get()
            except:
                pass
            
            try:
            # Xử lý đánh giá sao
                product_rating = response.xpath("//p[contains(@class, 'star-rating')]/@class").get()
                rating = product_rating.split()[-1] if product_rating else "No rating"
                star_ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
                stars = star_ratings.get(rating, "Không có đánh giá")
            except:
                pass

            try:
                image_url = response.xpath(
                    "//div[@class='thumbnail']/div[@class='carousel-inner']/div[@class='item active']\
                                           /img/@src").get()
                image_url = response.urljoin(image_url) if image_url else None
            except:
                pass

            # Tạo dữ liệu sản phẩm
            product_data = {
                'url': response.url,
                'product_name': product_name,
                'product_code': product_code,
                'product_type': product_type,
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