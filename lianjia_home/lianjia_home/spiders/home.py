# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider  # 导入Spider类

try:
    from ..items import LianjiaHomeItem
except ImportError:
    from lianjia_home.lianjia_home.items import LianjiaHomeItem  # 导入Item类


class HomeSpider(CrawlSpider):
    name = 'home'

    current_page = 1  # 记录当前的页数，默认为第1页
    total_page = 0  # 总页数

    cookie_str = "SECKEY_ABVK=czMe3tfgsEqKef7RjNH6HcCD3o/XnMnvQUxoXJAga9A%3D; BMAP_SECKEY=T5ZLrD3GomgXxPCQYdXs0XJwOA1cGLTXqX7XND6_b6nI98KwUshdRViOxPvMojm4giOLp-aBYNO7lHXMjP63fMqE4FOygw6THSmKKV-DlfgIYsY5LvAYz2EGyprho4uWBt_taPnfBI4vJMEtXvEzbypiiNPNailpgTx3RCrl33ZAFsB-k60DKiUccu51uby_; lianjia_uuid=d1ede39f-4c5b-4c22-8c68-05ebae648979; crosSdkDT2019DeviceId=-fzjejn-zbmw6e-s2wdjpt8d5dqgcm-94iyesaei; ftkrc_=60709932-1bca-4d55-9f81-73ced167aebc; lfrc_=710825ff-cb9a-486b-b841-79955c09af1b; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1741835654; HMACCOUNT=593038D2F646B4CD; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22194f3e66b72581-0814e2e34ca31d-26011a51-2073600-194f3e66b7311e6%22%2C%22%24device_id%22%3A%22194f3e66b72581-0814e2e34ca31d-26011a51-2073600-194f3e66b7311e6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ga=GA1.2.1142648427.1741835665; login_ucid=2000000155351372; lianjia_token=2.0013a9a7e17270b34102048ed0c7641a6c; lianjia_token_secure=2.0013a9a7e17270b34102048ed0c7641a6c; security_ticket=eIyt9Wp5NiwVnOPsqDMcGmhKZheq6UBYldXCwfrJW3aXnH3tv2mSD/0ZAucji0wkwlF5DjygUKeUgK0qr5SzTei+QBtqK1YkoMdqStZMJY7PcS33NB4N0fM7NbD4V8F3ckNbqsskXAIQbnDFm/wx9Py5YNOPzmriSty9zMJNs00=; lianjia_ssid=0208557f-d6f0-49b0-9ef1-67df173f8dd7; select_city=320500; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1742173661; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNmYyYTRhODg2ODE3ZGUzODVkYWQ4NTM1MmY5ZjliNWU3ZmJjMDUyOTg0YWRjYTUzNDhjNmQ1YmUxZTNmNTg0ZWNmYTVkNDNhZGVjNDA1Yzc1ZDQ5MTRmMjkzMjA3MDc5NTQxYTZjZGI1NjMyYWU2YTA2N2VjNjcyYjU3OTI5YzRjOWFjNjE3ODhiZTEwYjI3YjQ5YzU4MGZmYmU0OTU0ZDdhYWQ5MzY2ZmZjZDBhNDQyZTM5NDhlNmU4NmI4ZWEwZTViOGVlZjIxNmZkYTgzMWQwNzc3YWQ4M2Q0Y2RmYWY5MjJjNTNhYzhiMGViNTRiNjI3M2VjZDc2MzFiNTVlNVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI1NWM5Nzc2OFwifSIsInIiOiJodHRwczovL3N1LmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvMTA3MTEwNzI2OTI5Lmh0bWwiLCJvcyI6IndlYiIsInYiOiIwLjEifQ==; _gid=GA1.2.1014235912.1742173667; _gat=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _ga_NKCLMZHBXY=GS1.2.1742173667.4.1.1742173671.0.0.0"
    cookie_dict = {}
    items = cookie_str.split(';')
    for item in items:
        parts = item.strip().split('=')
        if len(parts) == 2:
            cookie_dict[parts[0]] = parts[1]

    # 设置用户代理（浏览器类型）
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br, zstd"
    }

    def start_requests(self):  # 获取初始请求
        url = "https://su.lianjia.com/ershoufang/"
        # 生成请求对象
        yield Request(url, headers=self.headers, callback=self.parse)

    # 如果从本文件执行，则导入pipelines，并设置ITEM_PIPELINES
    # settings 文件pipelines 是全局配置，如果有多个爬虫程序，需要设置 custom pipelines
    # try:
    #     from lianjia_home.lianjia_home.middlewares import LianjiaHomeDownloaderMiddleware
    #
    #     custom_settings = {
    #         'DOWNLOADER_MIDDLEWARES': {
    #             'lianjia_home.lianjia_home.middlewares.LianjiaHomeDownloaderMiddleware': 543,
    #             "scrapy.downloadermiddlewares.retry.RetryMiddleware": None  # 禁用默认的重试中间件，使用我们自定义的重试逻辑
    #         },
    #     }
    # except ImportError:
    #
    #     from ..middlewares import LianjiaHomeDownloaderMiddleware
    #     custom_settings = {
    #         'ITEM_PIPELINES': {
    #             'lianjia_home.middlewares.LianjiaHomeDownloaderMiddleware': 543,
    #             'scrapy.downloadermiddlewares.retry.RetryMiddleware': None
    #         },
    #     }

    def parse(self, response, **kwargs):  # 主页面解析函数
        # 1.提取主页中的房屋信息
        # 使用xpath定位到二手房信息的div元素，保存到列表中
        list_selecotr = response.xpath("//li/div[@class='info clear']")
        # 依次遍历每个选择器，获取二手房的名称、户型、面积、朝向等数据
        for one_selecotr in list_selecotr:
            try:
                # 获取房屋名称
                name = one_selecotr.xpath('div[@class="title"]/a/text()').get()
                # 获取其他信息
                other = one_selecotr.xpath('div[@class="address"]/div[@class="houseInfo"]/text()').get()
                # 以|作为间隔，转换为列表
                other_list = other.split("|")
                type = other_list[0].strip(" ")  # 户型
                area = other_list[1].strip(" ")  # 面积
                direction = other_list[2].strip(" ")  # 朝向
                fitment = other_list[3].strip(" ")  # 是否装修
                # 获取总价和单价，存入列表中
                price_list = one_selecotr.xpath("div[@class='priceInfo']//span/text()")
                # 总价
                total_price = price_list[0].extract()
                # 单价
                unit_price = price_list[1].extract()
                item = LianjiaHomeItem()  # 生成LianjiaHomeItem对象
                # 将已经获取的字段保存于item对象中
                item["name"] = name.strip(" ")  # 名称
                item["type"] = type  # 户型
                item["area"] = area  # 面积
                item["direction"] = direction  # 朝向
                item["fitment"] = fitment  # 是否装修
                item["total_price"] = total_price  # 总价
                item["unit_price"] = unit_price  # 单价
                # 2.获取详细页URL
                url = one_selecotr.xpath("div[@class='title']/a/@href").extract_first()
                # 3.生成详情页的请求对象，参数meta保存房屋部分数据
                yield Request(url, meta={"item": item}, callback=self.property_parse, headers=self.headers,
                              cookies=self.cookie_dict)
            except:
                pass
        # 4.获取下一页URL，并生成Request请求
        # (1)获取下一页URL。仅在解析第一页时获取总页数的值
        if self.current_page == 1:
            # 属性page-data的值中包含总页数和当前页
            self.total_page = response.xpath("//div[@class='page-box house-lst-page-box']/@page-data").re("\\d+")
            # 获取总页数
            self.total_page = int(self.total_page[0])
        self.current_page += 1  # 下一页的值
        if self.current_page <= self.total_page:  # 判断页数是否已越界
            next_url = "https://su.lianjia.com/ershoufang/pg%d" % self.current_page
            # (2)根据URL生成Request，使用yield提交给引擎
            yield Request(next_url, headers=self.headers, callback=self.parse)

    # 详细页解析函数
    def property_parse(self, response):
        # 1.提取房屋产权信息
        property = response.xpath(
            '//div[@class="introContent"]/div[2]/div[2]/ul/li[last()-2]/span[2]/text()').extract_first().strip()
        # 2.获取主页面中的房屋信息
        item = response.meta["item"]
        # 3.将产权信息添加到item中，返回给引擎
        item["property"] = property
        # 配备电梯
        elevator = response.xpath(
            '//div[@class="introContent"]/div[1]/div[2]/ul/li[last()]/text()').extract_first().strip()
        item["elevator"] = elevator
        yield item


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(HomeSpider)
    process.start()
