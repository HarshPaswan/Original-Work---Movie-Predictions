import random
import json
import locale
import urllib2
import re
import time
import scrapy
from bs4 import BeautifulSoup

from movieData.items import MovieItem

class MovieUrlsProvider():
    def _init_(self):
        pass

    def prepare_movie(self):
        with open("feth_imdb_url.json", "r") as x:
            movies = json.load(x)
        urls = [m['movie_imbd_link'] for m in movies]
        return urls

class ImdbExtract(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    start_urls = MovieUrlsProvider.prepare_movie()

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    def extract_text(self, xpath, response):
        path = "{}/text()".format(xpath)
        return response.xpath(path).extract()

    def facebook_likes(self, e_type, e_id):
        if e_type == "person_name_id":
            url = "https://www.facebook.com/widgets/like.php?width=280&show_faces=1&layout=standard&href=http%3A%2F%2Fwww.imdb.com%2Fname%2F{}%2F&colorscheme=light".format(e_id)
        elif e_type == "movie_title_id":
            url = "https://www.facebook.com/widgets/like.php?width=280&show_faces=1&layout=standard&href=http%3A%2F%2Fwww.imdb.com%2Ftitle%2F{}%2F&colorscheme=light".format(e_id)
        else:
            url = None

        time.sleep(random.uniform(0, 0.75))
        try:
            content = urllib2.urlopen(url).read()
            soup = BeautifulSoup(content, "lxml")
            sentence = soup.find_all(id = "u_0_2")[0].span.string
            likes = sentence.split(" ")[0]
        except Exception as e:
            likes = None
        return likes

    def id_from_url(self, url):
        if url is None:
            return None
        return re.search("(tt[0-9]{7})", url).group()

    def name_id_from_url(self, url):
        if url is None:
            return None
        return re.search("(nm[0-9]{7})", url).group()
    

    def parse(self, response):
        pass
    def parse(self, response):
        print("*"*100)
        item = MovieItem()
        item['movie_imdb_link'] = response.url

        try:
            m_title = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract()[0]
        except:
            m_title = None
        item['movie_title'] = m_title

       
        try:
            t_year = response.xpath('//*[@id="titleYear"]/a/text()').extract()[0]
        except:
            t_year = None
        item['title_year'] = t_year

        
        try:
            genres = response.xpath('//div[@itemprop="genre"]//a/text()').extract()
        except:
            genres = None
        item['genres'] = genres

       
        try:
            country = response.xpath('//div[@id="titleDetails"]/div/a[contains(@href, "country")]/text()').extract()
        except:
            country = None
        item['country'] = country

        
        try:
            language = response.xpath('//div[@id="titleDetails"]/div/a[contains(@href, "language")]/text()').extract()
        except:
            language = None
        item['language'] = language

        
        try:
            plot_keywords = response.xpath('//a/span[@itemprop="keywords"]/text()').extract()
        except:
            plot_keywords = None
        item['plot_keywords'] = plot_keywords

        
        try:
            storyline = response.xpath('//div[@id="titleStoryLine"]/div[@itemprop="description"]/p/text()').extract()[0]
        except:
            storyline = None
        item['storyline'] = storyline

        
        try:
            color = response.xpath('//a[contains(@href, "colors=")]/text()').extract()
        except:
            color = None
        item['color'] = color

        
        try:
            budget = response.xpath('//h4[contains(text(), "Budget:")]/following-sibling::node()/descendant-or-self::text()').extract()
        except:
            budget = None
        item['budget'] = budget

        
        try:
            gross = response.xpath('//h4[contains(text(), "Gross:")]/following-sibling::node()/descendant-or-self::text()').extract()
        except:
            gross = None
        item['gross'] = gross

        
        try:
            imdb_score = response.xpath("//span[@itemprop='ratingValue']/text()").extract()
        except:
            imdb_score = None
        item['imdb_score'] = imdb_score

        
        try:
            num_voted_users = response.xpath('//span[@itemprop="ratingCount"]/text()').extract()[0]
        except:
            num_voted_users = None
        item['num_voted_users'] = locale.atoi(num_voted_users)

        
        try:
            duration = response.xpath('//time[@itemprop="duration"]/text()').extract()
        except:
            duration = None
        item['duration'] = duration

        
        try:
            aspect_ratio = response.xpath('//h4[contains(text(), "Aspect Ratio:")]/following-sibling::node()/descendant-or-self::text()').extract()
            
            ratio = ""
            for s in aspect_ratio:
                s = s.strip()
                if len(s) != 0:
                    ratio = s
                    break
            aspect_ratio = ratio
        except:
            aspect_ratio = None
        
        item['aspect_ratio'] = aspect_ratio

        
        try:
            content_rating = response.xpath('//meta[@itemprop="contentRating"]/following-sibling::node()/descendant-or-self::text()').extract()
        except:
            content_rating = None
        item['content_rating'] = content_rating

        
        try:
            num_user_for_reviews = response.xpath('//span/a[contains(@href, "reviews")]/text()').extract()[0]
            num_user_for_reviews = locale.atoi(num_user_for_reviews.split(" ")[0])
        except:
            num_user_for_reviews = None
        item['num_user_for_reviews'] = num_user_for_reviews

        
        try:
            num_critic_for_reviews = response.xpath('//span/a[contains(@href, "externalreviews")]/text()').extract()[0]
            
            num_critic_for_reviews = locale.atoi(num_critic_for_reviews.split(" ")[0])
        except:
            num_critic_for_reviews = None
        item['num_critic_for_reviews'] = num_critic_for_reviews

        

        base_url = "http://www.imdb.com"

        try:
            
            cast_name_list_from_odd_rows = response.xpath('//table[@class="cast_list"]/tr[@class="odd"]/td[@class="itemprop"]/a/span[@class="itemprop"]/text()').extract()
            cast_name_href_list_from_odd_rows = response.xpath('//table[@class="cast_list"]/tr[@class="odd"]/td[@class="itemprop"]/a/@href').extract()
            links_from_odd_rows = [base_url + e for e in cast_name_href_list_from_odd_rows]
            pairs_for_odd_rows = zip(cast_name_list_from_odd_rows, links_from_odd_rows)

           
            cast_name_list_from_even_rows = response.xpath('//table[@class="cast_list"]/tr[@class="even"]/td[@class="itemprop"]/a/span[@class="itemprop"]/text()').extract()
            cast_name_href_list_from_even_rows = response.xpath('//table[@class="cast_list"]/tr[@class="even"]/td[@class="itemprop"]/a/@href').extract()
            links_from_even_rows = [base_url + e for e in cast_name_href_list_from_even_rows]
            pairs_for_even_rows = zip(cast_name_list_from_even_rows, links_from_even_rows)

            
            cast_name_link_pairs = pairs_for_odd_rows + pairs_for_even_rows

            cast_info = []
            for p in cast_name_link_pairs:
                name, link = p[0], p[1]
                actor = {}
                actor["actor_name"] = name
                actor["actor_link"] = link

                name_id = self.get_person_name_id_from_url(link)
                actor["actor_facebook_likes"] = self.get_facebook_likes(entity_type="person_name_id", entity_id=name_id)

                cast_info.append(actor)
        except:
            cast_info = None
        item['cast_info'] = cast_info
        try:
            director_name = response.xpath('//span[@itemprop="director"]/a/span/text()').extract()[0]

            director_partial_link = response.xpath('//span[@itemprop="director"]/a/@href').extract()[0]
            director_full_link = base_url + director_partial_link


            director_info = {}
            director_info["director_name"] = director_name
            director_info["director_link"] = director_full_link

            name_id = self.get_person_name_id_from_url(director_full_link)
            director_info["director_facebook_likes"] = self.get_facebook_likes(entity_type="person_name_id", entity_id=name_id)
        except:
            director_info = None
        item['director_info'] = director_info

        movie_id = self.get_movie_id_from_url(response.url)
        num_facebook_like = self.get_facebook_likes(entity_type="movie_title_id", entity_id=movie_id)
        item['num_facebook_like'] = num_facebook_like

        yield item
