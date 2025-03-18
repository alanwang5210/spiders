# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import redis  # 导入Redis库


class ProxyPipeline(object):
    # Spider开启时，获取数据库配置信息，连接Redis数据库服务器
    def open_spider(self, spider):
        if spider.name == "proxy":
            # (4)设置Redis数据库信息
            REDIS_HOST = "10.10.120.201"  # 主机地址
            REDIS_PORT = 30979  # 端口
            REDIS_DB_INDEX = 0  # 索引

            # 获取配置文件中Redis的配置信息
            host = spider.settings.get("REDIS_HOST", REDIS_HOST)  # 主机地址
            port = spider.settings.get("REDIS_PORT", REDIS_PORT)  # 端口
            db_index = spider.settings.get("REDIS_DB_INDEX", REDIS_DB_INDEX)  # 索引
            # 连接Redis，得到一个连接对象
            self.db_conn = redis.StrictRedis(host=host,  # 主机地址
                                             port=port,  # 端口
                                             db=db_index,  # 索引
                                             decode_responses=True)  # 获取字符串类型
            self.db_conn.delete("ip")

    # 将数据存储于Redis数据库中
    def process_item(self, item, spider):
        if spider.name == "proxy":
            # 将item转换为字典类型
            item_dict = dict(item)
            # 将item_dict保存于key为ip的集合中
            self.db_conn.sadd("ip", item_dict["url"])
        return item
