import scrapy
import json
from scrapy.selector import Selector
from movieData.items import MovieBudgetItem

class MovieListInitial(scrapy.Spider):
    name = "movie-budget"
    allowed_domains = ["the-numbers.com"]      #This is the primary domain we are using, so it is the only one we are allowing in order to decrease complexity

    start_urls = (
        'https://www.the-numbers.com/movie/budgets/all',             #direct url from which I will be extracting the movie data from
    )   

    def parse(self, response):
        base_link = 'http://www.the-numbers.com'

        print("="*50)   #creates sections to avoid confusion in output
        rows = response.xpath("//table/tr")                  #This is how we will search the HTML Document/site ----> //table/tr means that we have to search in tr which is stored in table

        #Iterating through the  odd rows
        for i, rownum in enumerate(rows):

            if i%2==0:
               continue #this keyword will end the for loop if the condition is met

            movie_budget_item = MovieBudgetItem()

            release_date = rownum.xpath('td/a/text()').extract()[0]     #This searches in td for the release date of the specified movie row number using text()
            partial_url = rownum.xpath('td/b/a/@href').extract()[0]    # gets the url part that goes after the base_link in order to specify the particular movie
            movie_link = base_link + partial_url
            movie_name = rownum.xpath('td/b/a/text()').extract()[0]

            #money
            budgets = rownum.xpath('td[@class="data"]/text()').extract()[1:] #gets the lines with all the budgets for one row ---> This is the row which we will dissect
            production_budget = budgets[0]
            domestic_gross = budgets[1]
            worldwide_gross = budgets[2]    

            #storing the variables for later access
            movie_budget_item['date'] = release_date
            movie_budget_item['link'] = movie_link
            movie_budget_item['movie_name'] = movie_name
            movie_budget_item['production_budget'] = production_budget
            movie_budget_item['domestic_gross'] = domestic_gross
            movie_budget_item['worldwide_gross'] = worldwide_gross
            print ("="*50)
            yield movie_budget_item
