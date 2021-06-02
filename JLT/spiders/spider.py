import scrapy

class PostsSpider(scrapy.Spider):
    name = "restaurant"

    start_urls = [
        'https://www.talabat.com/uae/restaurants/1308/jumeirah-lakes-towers-jlt'
    ]

    def parse(self, response):
        for restaurant in response.css('div.restaurant-info-section'):
            yield {
                
                'brand_name': restaurant.css('.restaurant-title h2::text').get(),
                'cuisine_tags': restaurant.css('.cuisines-section .f-14::text').getall(),
                'restaurant_rating':restaurant.css('.ml-1::text').get(),
                'delivery_time':((restaurant.css('.info-section .mr-2::text').get()).strip('Within ')).strip(' mins'),
                'service_fee':restaurant.css('.info-section .mr-2::text')[1].get(),
                'minimum_order_amount':restaurant.css('.d-none::text')[2].get(),
                'new_restaurant':restaurant.css('.new-restaurant-label::text').get(),
                                   

            }
        # go to the next page     
        next_page =  response.xpath('//*[@id="__next"]/div[5]/div/div/div[2]/div[2]/div[3]/div/ul/li[22]/a/@href').get()
        if next_page is not None:
           next_page = response.urljoin(next_page)
           yield scrapy.Request(next_page, callback=self.parse)
            