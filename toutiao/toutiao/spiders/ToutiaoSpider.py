from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from selenium import webdriver  # 导入浏览器引擎模块

try:
    from ..items import ToutiaoItem  # 导入Item模块
except ImportError:
    from toutiao.toutiao.items import ToutiaoItem


class ToutiaoSpider(Spider):
    # 定义爬虫名称
    name = 'toutiao'

    # 构造函数
    def __init__(self, name: str | None = None, **kwargs):
        super().__init__(name, **kwargs)

        # 生成chrom的对象driver
        self.driver = webdriver.Chrome()

    # 获取初始Request
    def start_requests(self):
        url = "https://www.toutiao.com/?channel=hot&source=ch"
        # 生成请求对象，设置url
        yield Request(url, callback=self.parse)

        # 如果从本文件执行，则导入pipelines，并设置ITEM_PIPELINES

    # settings 文件pipelines 是全局配置，如果有多个爬虫程序，需要设置 custom pipelines
    try:
        from toutiao.toutiao.middlewares import ToutiaoDownloaderMiddleware

        custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'toutiao.toutiao.middlewares.ToutiaoDownloaderMiddleware': 543
            },
        }
    except ImportError:

        from ..middlewares import ToutiaoDownloaderMiddleware
        custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'toutiao.middlewares.ToutiaoDownloaderMiddleware': 543
            },
        }

    # 数据解析方法

    # 数据解析方法
    def parse(self, response, **kwargs):
        print("---------------------------------------------------")
        item = ToutiaoItem()
        list_selector = response.xpath("//div[@class='feed-card-article-l']")
        for li in list_selector:
            try:
                # 标题
                title = li.xpath(".//a[@class='title']/text()").get()
                # 来源
                source = li.xpath(".//div[@class='feed-card-footer-cmp-author']/a/text()").get()
                # 评论数
                comment = li.xpath(".//div[@class='feed-card-footer-comment-cmp']/a/text()").get()
                item["title"] = title  # 标题
                item["source"] = source  # 来源
                item["comment"] = comment  # 评论数
                yield item
            except:
                continue


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ToutiaoSpider)
    process.start()
