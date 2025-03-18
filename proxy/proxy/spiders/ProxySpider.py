# -*-coding:utf-8-*-
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from proxy.proxy.items import ProxyItem
import json


class ProxySpider(Spider):
    name = 'proxy'  # 爬虫名称

    def __init__(self):
        self.test_url = 'https://www.gushiwen.cn'  # 从命令中获取测试网站的URL
        self.current_page = 1  # 当前页，设置为1

    # 获取初始Request
    def start_requests(self):
        url = 'https://proxy.scdn.io/api/proxy_list.php?page=1&per_page=100&type=&country='  # 西刺代理高匿URL地址
        # 生成请求对象
        yield Request(url)

    # 如果从本文件执行，则导入pipelines，并设置ITEM_PIPELINES
    # settings 文件pipelines 是全局配置，如果有多个爬虫程序，需要设置 custom pipelines
    try:
        from proxy.proxy.pipelines import ProxyPipeline

        custom_settings = {
            'ITEM_PIPELINES': {
                'proxy.proxy.pipelines.ProxyPipeline': 543
            },
        }
    except ImportError:

        from ..pipelines import ProxyPipeline
        custom_settings = {
            'ITEM_PIPELINES': {
                'proxy.pipelines.ProxyPipeline': 543
            },
        }

    # 解析函数
    # 1.提取西刺代理高匿URL地址
    # 2.验证代理URL的有效性
    def parse(self, response, **kwargs):
        datas = json.loads(response.text)

        # 依次读取每条代理的信息，从中获取IP、端口和类型
        for data in datas['data']['proxies']:
            # Item对象
            item = ProxyItem()
            # 获取IP
            ip = data['ip']
            # 获取端口
            port = data['port']
            # 获取类型（http或https）
            http = data['type'].lower()
            # 拼接成完整的代理URL
            url = "{}://{}:{}".format(http, ip, port)
            item["url"] = url
            # 使用代理服务器向测试网站发送Request请求
            yield Request(self.test_url,  # 测试网站的url
                          callback=self.test_parse,  # 回调函数
                          errback=self.error_back,  # 异常处理函数
                          meta={"proxy": url,  # 代理服务器地址
                                "dont_retry": True,  # 执行一次请求
                                "download_timeout": 10,  # 超时时间
                                "item": item},  # 传递的参数
                          dont_filter=True  # 不过滤重复请求
                          )
        if self.current_page <= 5:  # 爬取5页代理信息
            # 获取下一页URL
            next_page = self.current_page + 1
            next_url = f"https://proxy.scdn.io/api/proxy_list.php?page={next_page}&per_page=100&type=&country="
            self.current_page += 1
            yield Request(next_url)

    # 回调函数
    def test_parse(self, response):
        # 获取item并yield
        yield response.meta["item"]

    # 异常处理函数
    def error_back(self, failure):
        # 打印错误日志信息
        self.logger.error(repr(failure))


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ProxySpider)
    process.start()
