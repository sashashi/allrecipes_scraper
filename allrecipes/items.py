# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Recipe(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    rating_count = scrapy.Field()
    comment_count = scrapy.Field()
    ingredient_names = scrapy.Field()
    ingredient_quantities = scrapy.Field()
    ingredient_units = scrapy.Field()
    servings_per_recipe = scrapy.Field()
    calories_per_serving = scrapy.Field()
    total_fat_dv = scrapy.Field()
    saturated_fat_dv = scrapy.Field()
    cholesterol_dv = scrapy.Field()
    sodium_dv = scrapy.Field()
    total_carbohydrate_dv = scrapy.Field()
    dietary_fiber_dv = scrapy.Field()
    vitamin_c_dv = scrapy.Field()
    calcium_dv = scrapy.Field()
    iron_dv = scrapy.Field()
    potassium_dv = scrapy.Field()
    total_sugars = scrapy.Field()
    protein = scrapy.Field()
