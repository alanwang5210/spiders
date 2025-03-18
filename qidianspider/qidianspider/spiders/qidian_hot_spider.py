from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider

from scrapy.loader import ItemLoader  # 导入ItemLoader类

try:
    from ..items import GuShiWenItem
except ImportError:
    from qidianspider.qidianspider.items import GuShiWenItem


class HotSalesSpider(CrawlSpider):
    name = 'hot_sales'
    allowed_domains = ['gushiwen.cn']
    # 起始URL
    start_urls = ['https://www.gushiwen.cn/shiwens/default.aspx?cstr=%e5%85%88%e7%a7%a6']

    current_page = 1  # 设置当前页，起始为1

    # 设置用户代理（浏览器类型）
    # qidian_headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    #     "Accept-Encoding": "gzip, deflate, br, zstd"
    # }

    # 获取初始Request
    def start_requests(self):
        url = "https://www.gushiwen.cn/shiwens/default.aspx?cstr=%e5%85%88%e7%a7%a6"
        # 生成请求对象，设置url，headers，callback
        yield Request(url, callback=self.parse)

    # 如果从本文件执行，则导入pipelines，并设置ITEM_PIPELINES
    # settings 文件pipelines 是全局配置，如果有多个爬虫程序，需要设置 custom pipelines
    try:
        from qidianspider.qidianspider.pipelines import QidianspiderPipeline

        custom_settings = {
            'ITEM_PIPELINES': {
                'qidianspider.qidianspider.pipelines.QidianspiderPipeline': 300,
                'qidianspider.qidianspider.pipelines.DuplicatesPipeline': 299,
                'qidianspider.qidianspider.pipelines.SaveToTxtPipeline': 298,
            },
        }
    except ImportError:

        from ..pipelines import QidianspiderPipeline
        custom_settings = {
            'ITEM_PIPELINES': {
                'qidianspider.pipelines.QidianspiderPipeline': 300,
                'qidianspider.pipelines.DuplicatesPipeline': 299,
                'qidianspider.pipelines.SaveToTxtPipeline': 298,
            },
        }

    def parse(self, response, **kwargs):
        if response:
            print('----------------------------------------------')
            print(response.request.headers)
            # 获取每个排行榜的URL
            list_selector = response.xpath('//div[contains(@id,"zhengwen")]')

            for selector in list_selector:
                item = ItemLoader(item=GuShiWenItem(), selector=selector)
                item.add_xpath('title', 'p[1]/a/b/text()')
                item.add_xpath('author', 'p[2]/a[1]/text()')
                item.add_value('chaidai', selector.xpath('p[2]/a[2]/text()').get().replace('〔', '').replace('〕', ''))
                item.add_value('content', '\n'.join(selector.xpath('div[@class="contson"]/text()').getall()).strip())
                yield item.load_item()

            # 获取下一页URL，并生成Request请求，提交给引擎
            # 1.获取下一页URL
            self.current_page += 1
            if self.current_page <= 2:
                next_url = f"https://www.gushiwen.cn/shiwens/default.aspx?tstr=&astr=&cstr=%e5%85%88%e7%a7%a6&xstr=&page={self.current_page}"
                # 2.根据URL生成Request，使用yield返回给引擎
                yield Request(next_url, callback=self.parse)
        else:
            print("Response is empty")


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(HotSalesSpider)
    process.start()
