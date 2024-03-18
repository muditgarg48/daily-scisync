import scrapy

class SmithsonianSpider(scrapy.Spider):
    name = "smithsonian"
    start_urls = [
        'https://www.smithsonianmag.com/category/archaeology/',
        'https://www.smithsonianmag.com/category/us-history/',
        'https://www.smithsonianmag.com/category/world-history/',
        'https://www.smithsonianmag.com/category/human-behavior/',
        'https://www.smithsonianmag.com/category/mind-body/',
        'https://www.smithsonianmag.com/category/our-planet/',
        'https://www.smithsonianmag.com/category/space/',
        'https://www.smithsonianmag.com/category/wildlife/',
        'https://www.smithsonianmag.com/category/education/',
        'https://www.smithsonianmag.com/category/energy/',
        'https://www.smithsonianmag.com/category/health-medicine/',
        'https://www.smithsonianmag.com/category/technology/',
        'https://www.smithsonianmag.com/category/art-artists/',
        'https://www.smithsonianmag.com/category/books-2/',
        'https://www.smithsonianmag.com/category/design/',
        'https://www.smithsonianmag.com/category/food/',
        'https://www.smithsonianmag.com/category/music-film/',
        'https://www.smithsonianmag.com/category/africa-middleeast/',
        'https://www.smithsonianmag.com/category/asia-pacific/',
        'https://www.smithsonianmag.com/category/europe/',
        'https://www.smithsonianmag.com/category/central-south-america/',
        'https://www.smithsonianmag.com/category/us-canada/',
    ]

    def parse(self, response):
        for article in response.css('div.article-list-text'):
            link = article.css('h3 a::attr(href)').get()
            yield response.follow(link, self.parse_article, meta={
                'title': article.css('h3 a::text').get(),
                'link': link,
            })

        for i in range(2, 21):
            next_page = response.urljoin(f'?page={i}')
            yield scrapy.Request(next_page, self.parse)

    def parse_article(self, response):
        title = response.meta['title']
        link = response.meta['link']
        description = response.css('meta[name="description"]::attr(content)').get()
        section = response.css('meta[property="article:section"]::attr(content)').get()
        tags = response.css('meta[property="article:tag"]::attr(content)').get()
        yield {
            'title': title,
            'link': link,
            'description': description,
            'section': section,
            'tags': tags,
        }
