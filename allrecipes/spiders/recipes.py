import scrapy
from scrapy.spiders import CrawlSpider, Rule, SitemapSpider
from scrapy.linkextractors import LinkExtractor
import time
from allrecipes.items import Recipe
from scrapy_selenium import SeleniumRequest
import re

def wait(driver):
    time.sleep(1)
    return True

class RecipesSpider(SitemapSpider):
    name = 'recipes'
    allowed_domains = ['allrecipes.com']
    sitemap_urls = ['https://www.allrecipes.com/sitemap_1.xml']
    #, 'https://www.allrecipes.com/sitemap_2.xml', 'https://www.allrecipes.com/sitemap_3.xml', 'https://www.allrecipes.com/sitemap_4.xml'
    sitemap_rules = [('/recipe/', 'parse_recipe')]

    def make_request_from_url(self, url):
        return SeleniumRequest(url=url, wait_time=10, wait_until=wait)
        
    def parse_recipe(self, response):
        recipe = Recipe()
        recipe['url'] = response.url
    
        recipe['title'] = response.xpath('//h1[@id="article-heading_1-0"]/text()').get().strip('\n ')

        recipe['description'] = response.xpath('//h2/text()').get().strip('\n ')

        recipe['rating'] =  response.xpath('//div[@id="mntl-recipe-review-bar__rating_1-0"]/text()').get()
        if recipe['rating'] != None:
            recipe['rating'] = recipe['rating'].strip('\n ')

        recipe['rating_count'] =  response.xpath('//div[@id="mntl-recipe-review-bar__rating-count_1-0"]/text()').get()
        if recipe['rating_count'] != None:
            recipe['rating_count'] = recipe['rating_count'][2:len(recipe['rating_count'])-1]
            
        recipe['comment_count'] =  response.xpath('//div[@id="mntl-recipe-review-bar__comment-count_1-0"]/text()').get()
        if recipe['comment_count'] != None:
            recipe['comment_count'] = recipe['comment_count'][1:len(recipe['comment_count'])-7].strip(' ')

        recipe['ingredient_names'] = list(map(lambda x:x.strip('\n '), response.xpath('//div[@id="mntl-structured-ingredients_1-0"]//span[@data-ingredient-name="true"]/text()').getall()))

        recipe['ingredient_quantities'] = response.xpath('//div[@id="mntl-structured-ingredients_1-0"]//span[@data-ingredient-quantity="true"]/text()').getall()

        recipe['ingredient_units'] = response.xpath('//div[@id="mntl-structured-ingredients_1-0"]//span[@data-ingredient-unit="true"]/text()').getall()
        
        recipe['servings_per_recipe'] = response.xpath('//tr[@class="mntl-nutrition-facts-label__servings"]//span[2]/text()').get()
        
        recipe['calories_per_serving'] = response.xpath('//tr[@class="mntl-nutrition-facts-label__calories"]//span[2]/text()').get()
        
        recipe['total_fat_dv'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Saturated Fat"]/parent::td/following-sibling::td[1]/text()').get()
        if recipe['total_fat_dv'] != None:
            recipe['total_fat_dv'] = float(recipe['total_fat_dv'].strip('\n ')[:-1])/100
        
        recipe['saturated_fat_dv'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Cholesterol"]/parent::td/following-sibling::td[1]/text()').get()
        if recipe['saturated_fat_dv'] != None:
            recipe['saturated_fat_dv'] = float(recipe['saturated_fat_dv'].strip('\n ')[:-1])/100
                
        recipe['cholesterol_dv'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Cholesterol"]/parent::td/following-sibling::td[1]/text()').get()
        if recipe['cholesterol_dv'] != None:
            recipe['cholesterol_dv'] = float(recipe['cholesterol_dv'].strip('\n ')[:-1])/100
        
        recipe['sodium_dv'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Sodium"]/parent::td/following-sibling::td[1]/text()').get()
        if recipe['sodium_dv'] != None:
            recipe['sodium_dv'] = float(recipe['sodium_dv'].strip('\n ')[:-1])/100
            
        recipe['total_carbohydrate_dv'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Total Carbohydrate"]/parent::td/following-sibling::td[1]/text()').get()
        if recipe['total_carbohydrate_dv'] != None:
            recipe['total_carbohydrate_dv'] = float(recipe['total_carbohydrate_dv'].strip('\n ')[:-1])/100
            
        recipe['dietary_fiber_dv'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Dietary Fiber"]/parent::td/following-sibling::td[1]/text()').get()
        if recipe['dietary_fiber_dv'] != None:
            recipe['dietary_fiber_dv'] = float(recipe['dietary_fiber_dv'].strip('\n ')[:-1])/100
            
        recipe['vitamin_c_dv'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Vitamin C"]/parent::td/following-sibling::td[1]/text()').get()
        if recipe['vitamin_c_dv'] != None:
            recipe['vitamin_c_dv'] = float(recipe['vitamin_c_dv'].strip('\n ')[:-1])/100
            
        recipe['calcium_dv'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Calcium"]/parent::td/following-sibling::td[1]/text()').get()
        if recipe['calcium_dv'] != None:
            recipe['calcium_dv'] = float(recipe['calcium_dv'].strip('\n ')[:-1])/100
            
        recipe['iron_dv'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Iron"]/parent::td/following-sibling::td[1]/text()').get()
        if recipe['iron_dv'] != None:
            recipe['iron_dv'] = float(recipe['iron_dv'].strip('\n ')[:-1])/100
            
        recipe['potassium_dv'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Potassium"]/parent::td/following-sibling::td[1]/text()').get()
        if recipe['potassium_dv'] != None:
            recipe['potassium_dv'] = float(recipe['potassium_dv'].strip('\n ')[:-1])/100
            
        recipe['total_sugars'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Total Sugars"]/following-sibling::text()[1]').get()
        if recipe['total_sugars'] != None:
            recipe['total_sugars'] = recipe['total_sugars'].strip('\n')[:-1]
            
        recipe['protein'] = response.xpath('//tbody[@class="mntl-nutrition-facts-label__table-body type--cat"]//span[text()="Protein"]/following-sibling::text()[1]').get()
        if recipe['protein'] != None:
            recipe['protein'] = recipe['protein'].strip('\n')[:-1]
            
        return recipe
