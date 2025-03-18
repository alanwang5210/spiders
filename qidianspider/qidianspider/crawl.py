"""
调用scrapy 命令行执行爬虫
crawl url -> crawl view -> crawl fan_yi
"""
import os
import sys

from scrapy import cmdline
from scrapy.cmdline import execute


def crawl_view():
    """
    爬取网页标题、正文，提取附件链接
    :return:
    """
    print("Crawling view...")
    cmdline.execute("scrapy crawl hot_sales".split())

    #添加当前项目的绝对地址
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    #执行 scrapy 内置的函数方法execute，  使用 crawl 爬取并调试，最后一个参数jobbole 是我的爬虫文件名
    execute(['scrapy', 'crawl', 'qidian'])


if __name__ == '__main__':
    crawl_view()
