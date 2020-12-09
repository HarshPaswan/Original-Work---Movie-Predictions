import scrapy 
import json
import urllib2
from scrapy.selector import Selector
from movieData.items import ImdbUrlItem

class ProvideURL():
    def _init_(self):
        pass
    def prepare(self):
        with open("movie_budget.json", "r") as i:
            movie = json.load(i)

            urls = []
            for x in movie:
                title = x['movie_name']
                url_title = urllib2.quote(title.encode('utf-8'))
                imdb_links = "http://www.imdb.com/find?ref_=nv_sr_fn&q={}&s=tt".format(url_title)
                urls.append(imdb_links)
            
            return urls


class ImdbSpiderUrl(scrapy.Spider):
    name = "imdb_url"
    allowed_domain = ["imdb.com"]
    start_urls = ProvideURL().prepare()

    def parse(self, response):
        item = ImdbUrlItem()

        first_movie = response.xpath("//table[@class='findList']/tr/td[@class='result_text']/a/@href").extract()[0]
        full_url = "http://www.imdb.com" + first_movie

        item['movie_name'] = response.xpath("//table[@class='findList']/tr/td[@class='result_text']/a/text()").extract()[0]
        item['movie_imdb_link'] = full_url

        yield item