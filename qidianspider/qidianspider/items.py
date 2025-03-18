# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst


class QidianspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def title_convert(title):
    return title[0].strip()

def author_convert(author):
    return author[0].strip()

# 保存小说热销榜字段数据
class GuShiWenItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(output_processor=title_convert)  # 小说名称
    author = scrapy.Field(output_processor=author_convert)  # 作者
    chaidai = scrapy.Field(output_processor=TakeFirst())  # 类型
    content = scrapy.Field(output_processor=TakeFirst())  # 形式
