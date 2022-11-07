# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AllrecipesPipeline:
    def process_item(self, recipe, spider):
        return recipe

class CleanIngredientQuantitiesPipeline:
    def process_item(self, recipe, spider):
        vulgar_frac_dict = {'½': '1/2', '⅓': '1/3', '⅔': '2/3', '¼': '1/4', '¾': '3/4', '⅕': '1/5', '⅖': '2/5', '⅗': '3/5', '⅘': '4/5', '⅙': '1/6', '⅚': '5/6', '⅐': '1/7', '⅛': '1/8', '⅜': '3/8', '⅝': '5/8', '⅞': '7/8', '⅑': '1/9', '⅒': '1/10'}
        for i in range(0, len(recipe['ingredient_quantities'])):
            recipe['ingredient_quantities'][i]=' '.join([vulgar_frac_dict.get(x, x) for x in recipe['ingredient_quantities'][i].split()])
        def mixed_to_improper(s):
            if ' ' in s:
                a,b=s.split()
                b,c=b.split('/')
                return '%s/'%(int(a)*int(c)+int(b))+c
            else:
                return s
        recipe['ingredient_quantities'] = list(map(mixed_to_improper, recipe['ingredient_quantities']))
        return recipe
