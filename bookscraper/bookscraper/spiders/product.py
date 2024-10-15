import scrapy

class ProductSpider(scrapy.Spider):
    name = "product"  # Đảm bảo tên spider là 'product'
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        # Vòng lặp qua các sản phẩm
        for product in response.xpath("//ol[@class='row']/li"):
            link = product.xpath(".//h3/a/@href").get()  # Lấy link sách
            full_link = response.urljoin(link)  # Tạo link đầy đủ từ URL tương đối
            yield {
                'link': full_link,
            }

        # Lấy link trang tiếp theo
        nextpage = response.xpath("//ul[@class='pager']/li[@class='next']/a/@href").get()

        # Nếu có trang tiếp theo, gửi yêu cầu đến đó và tiếp tục thu thập dữ liệu
        if nextpage:
            next_page_url = response.urljoin(nextpage)
            yield scrapy.Request(url=next_page_url, callback=self.parse)