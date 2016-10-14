import scrapy
import urlparse
from bs4 import BeautifulSoup
#link
class Article(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()


class MentalFlossArticles(scrapy.Spider):
    name = 'entelechy'
    dont_filter=True

    def __init__(self, cat=None):
        articles_url_base = 'http://entelechy.daiict.ac.in/public_html/entelechy_v2'
        if cat == 'books':
            cat = '8'

        if cat == 'cc':
            cat = '2'

        if cat == 'films':
            cat = '6'

        if cat == 'food':
            cat = '15'

        if cat == 'pictures':
            cat = '11'

        if cat == 'gna':
            cat = '4'

        if cat == 'music':
            cat = '7'

        if cat == 'random':
            cat = '10'

        if cat == 'sss':
            cat = '12'

        if cat == 'sports':
            cat = '5'

        if cat == 'tachyon':
            cat = '3'

        if cat == 'vuelo':
            cat = '9'

        if cat == 'interview':
            cat = '13'

        articles_url = articles_url_base
        if cat:
            articles_url = articles_url_base + '/?cat=' + cat

        self.start_urls = [articles_url]

    def parse(self, response):
        """Gets the page with the article list,
        find the article links and generates
        requests for each article page
        """
        article_links = response.xpath("//*[@id='main-content']/div[1]/div[2]//article/h2/a/@href").extract()
        #print article_links
        for link in article_links:
            article_url = urlparse.urljoin(response.url, link)
            yield scrapy.Request(article_url,self.extract_article)

    def extract_article(self, response):
        """Gets the article page and extract
        an item with the article data
        """
        article = Article()

        xpath = lambda s: response.xpath(s).extract()

        article['link'] = response.url
        article['title'] = xpath("//*[@id='main-content']/div[1]/article/div[2]/h1/div/text()")
        due = xpath('//*[@id="main-content"]/div[1]/article/div[2]/div[2]/div[1]')
        soup = BeautifulSoup(str(due), 'html.parser')
        due2 = soup.get_text().decode('unicode_escape').encode('ascii','ignore')
        article['content'] = due2.replace("\n"," ")
        article['author'] = xpath("//*[@id='main-content']/div[1]/article/div[2]/div[3]/strong/a/text()")

        yield article