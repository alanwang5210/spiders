# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaHomeItem(scrapy.Item):
    name = scrapy.Field()  # 名称
    type = scrapy.Field()  # 户型
    area = scrapy.Field()  # 面积
    direction = scrapy.Field()  # 朝向
    fitment = scrapy.Field()  # 装修情况
    elevator = scrapy.Field()  # 有无电梯
    total_price = scrapy.Field()  # 总价
    unit_price = scrapy.Field()  # 单价
    property = scrapy.Field()  # 产权信息
