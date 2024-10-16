import scrapy

class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    # Hàm để lấy link từng sản phẩm
    def parse(self, response):
        # Tạo vòng lặp để lập qua các link sản phẩm 
        for product_link in response.xpath("//ol[@class='row']/li"):
            link = product_link.xpath(".//h3/a/@href").get()  # Lấy link sách
            full_link = response.urljoin(link)  # Tạo link đầy đủ từ URL tương đối
            
            # Gửi yêu cầu đến trang chi tiết sản phẩm và gọi hàm parse_name để cào dữ liệu
            yield scrapy.Request(url=full_link, callback=self.parse_name)

        # Lấy link trang tiếp theo
        next_page = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)  # Tạo link đầy đủ từ URL tương đối
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    # Hàm chi tiết sản phẩm 
    def parse_name(self, response):
        # Lấy từng thuộc tính sản phẩm từ trang chi tiết sản phẩm
        product_name = response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get()
        product_code = response.xpath("//table[@class='table table-striped']//th[text()='UPC']/following-sibling::td/text()").get()
        product_type = response.xpath("//table[@class='table table-striped']//th[text()='Product Type']/following-sibling::td/text()").get()
        product_price =response.xpath("//table[@class='table table-striped']//th[text()='Price (excl. tax)']/following-sibling::td/text()").get()
        product_price_tax =response.xpath("//table[@class='table table-striped']//th[text()='Price (incl. tax)']/following-sibling::td/text()").get()
        tax = response.xpath("//table[@class='table table-striped']//th[text()='Tax']/following-sibling::td/text()").get()
        product_available =response.xpath("//table[@class='table table-striped']//th[text()='Availability']/following-sibling::td/text()").get()
        # Trả về thuộc tính sản phẩm và link tương ứng
        yield {
            'url': response.url,
            'product_name': product_name,
            'product_code': product_code,
            'product_type': product_type,
            'product_price_excl.tax': product_price,
            'product_price_incl.tax': product_price_tax,
            'tax': tax,
            'product_available': product_available
        }