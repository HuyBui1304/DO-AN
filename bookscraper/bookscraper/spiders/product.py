import scrapy
import pandas as pd

class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    # Khởi tạo danh sách để lưu dữ liệu
    data = []

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

        # Lưu dữ liệu vào danh sách
        self.data.append({
            'url': response.url,
            'product_name': product_name,
            'product_code': product_code,
            'product_type': product_type,
            'product_price_excl_tax': product_price,
            'product_price_incl_tax': product_price_tax,
            'tax': tax,
            'product_available': product_available
        })

    def close(self, reason):
        df = pd.DataFrame(self.data)
        df.to_excel('output.xlsx', index=False)