import scrapy


class FahasaTrendingSpider(scrapy.Spider):
    name = 'fahasa_trending'
    start_urls = ['https://www.fahasa.com/bestsellers']

    def parse(self, response):
        # Tìm tất cả các sản phẩm
        products = response.css('.product-item')

        for product in products:
            yield {
                'title': product.css('.product-title a::text').get().strip(),
                'price': product.css('.price::text').get().strip(),
                'link': product.css('.product-title a::attr(href)').get()
            }

        # Điều hướng sang trang tiếp theo (nếu có)
        next_page = response.css('.next::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

# Tắt kiểm tra robots.txt để không bị chặn
ROBOTSTXT_OBEY = False

# Thêm User-Agent để giả lập yêu cầu từ trình duyệt thực
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'

# Thêm độ trễ giữa các yêu cầu để tránh bị chặn
DOWNLOAD_DELAY = 1
