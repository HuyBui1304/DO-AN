import scrapy


class FahasaTrendingSpider(scrapy.Spider):
    name = 'fahasa_trending'
    start_urls = ['https://www.fahasa.com/bestsellers']

    def parse(self, response):
        # Truy xuất danh sách các sản phẩm từ trang
        products = response.css('.product-item')

        for product in products:
            yield {
                'title': product.css('.product-title a::text').get(),
                'price': product.css('.price::text').get(),
                'link': product.css('.product-title a::attr(href)').get()
            }

        # Truy cập trang tiếp theo nếu có
        next_page = response.css('.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
