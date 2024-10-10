import scrapy

class SanphamSpider(scrapy.Spider):
    name = "sanpham"  # Đây là tên bạn sẽ sử dụng để gọi spider

    allowed_domains = ["web.archive.org"]
    start_urls = ["https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html/"]

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div/li"):
            title = product.xpath(".//a[@class='p_box_title']/text()").get()
            yield {
                'title': title
            }
