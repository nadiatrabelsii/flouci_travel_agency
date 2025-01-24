import scrapy
from travel_scraper.items import TravelScraperItem
import random

# Define your proxy list
PROXY_LIST = [
    'http://216.229.112.25:8080',
    'http://89.58.50.94:3128'
]

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['travelandleisure.com']
    start_urls = ['https://www.travelandleisure.com/']

    def start_requests(self):
        for url in self.start_urls:
            proxy = random.choice(PROXY_LIST)  
            yield scrapy.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'},
                meta={'proxy': proxy}
            )

    def parse(self, response):
        print(f"Response URL: {response.url}")
        print(f"Response Status: {response.status}")
        print(f"Response Body: {response.text[:500]}")  

        # Scrape articles
        articles = response.css('article')
        if not articles:
            self.logger.warning("No articles found. Check your selectors or the website structure.")
        else:
            for article in articles:
                item = TravelScraperItem()
                item['title'] = article.css('h2::text').get(default="No title")
                item['url'] = response.urljoin(article.css('a::attr(href)').get(default="#"))
                item['summary'] = article.css('p::text').get(default="No summary")
                yield item

        # Handle pagination
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            self.logger.info(f"Next page found: {next_page}")
            yield response.follow(next_page, self.parse)
        else:
            self.logger.info("No next page found.")
