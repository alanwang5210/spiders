# -*- coding: utf-8 -*-
# 验证码处理测试脚本

import os
import sys
import requests
from urllib.parse import urljoin
from datetime import datetime

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入爬虫相关模块
from lianjia_home.middlewares import LianjiaHomeDownloaderMiddleware


def test_captcha_handling():
    """测试验证码处理功能"""
    print("开始测试验证码处理功能...")
    
    # 创建中间件实例
    middleware = LianjiaHomeDownloaderMiddleware()
    
    # 模拟爬虫和请求对象
    class MockSpider:
        def __init__(self):
            self.name = "test_spider"
            self.logger = MockLogger()
    
    class MockLogger:
        def info(self, msg):
            print(f"[INFO] {msg}")
        
        def warning(self, msg):
            print(f"[WARNING] {msg}")
        
        def error(self, msg):
            print(f"[ERROR] {msg}")
    
    class MockRequest:
        def __init__(self, url):
            self.url = url
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
            }
            self.meta = {}
            self.cookies = {}
    
    class MockResponse:
        def __init__(self, url, body, status=200):
            self.url = url
            self.body = body
            self.status = status
            self.text = body.decode('utf-8') if isinstance(body, bytes) else body
        
        def xpath(self, selector):
            # 简单模拟xpath功能，实际使用时需要使用lxml或scrapy的选择器
            return MockSelector()
    
    class MockSelector:
        def get(self):
            # 模拟返回验证码图片URL
            return "/captcha/image.jpg"
        
        def extract_first(self):
            return "/captcha/image.jpg"
    
    # 创建测试目录
    captcha_dir = os.path.join(os.getcwd(), 'captcha')
    if not os.path.exists(captcha_dir):
        os.makedirs(captcha_dir)
    
    # 创建模拟验证码图片
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    img_path = os.path.join(captcha_dir, f'test_captcha_{timestamp}.png')
    
    # 创建一个简单的验证码图片（1x1像素的黑色图片）
    with open(img_path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82')
    
    # 创建模拟验证码页面HTML
    html_path = os.path.join(captcha_dir, f'test_captcha_page_{timestamp}.html')
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>验证码测试页面</title>
    </head>
    <body>
        <h1>请输入验证码</h1>
        <form action="/verify" method="post">
            <img src="/captcha/image.jpg" alt="验证码" />
            <input type="text" name="captcha" placeholder="请输入验证码" />
            <input type="submit" value="提交" />
        </form>
    </body>
    </html>
    '''
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 创建模拟响应对象
    mock_response = MockResponse(
        url="https://su.lianjia.com/verify",
        body=html_content.encode('utf-8')
    )
    
    # 创建模拟请求对象
    mock_request = MockRequest(url="https://su.lianjia.com/ershoufang/")
    
    # 创建模拟爬虫对象
    mock_spider = MockSpider()
    
    # 测试验证码检测
    print("\n测试验证码页面检测...")
    is_captcha = middleware._is_captcha_page(mock_response)
    print(f"是否为验证码页面: {is_captcha}")
    
    # 测试验证码图片提取
    print("\n测试验证码图片URL提取...")
    img_url = middleware._extract_captcha_image_url(mock_response)
    print(f"提取的验证码图片URL: {img_url}")
    
    # 测试手动验证码处理
    print("\n测试手动验证码处理...")
    result = middleware._handle_captcha_manually(mock_response, mock_request, mock_spider)
    print(f"手动处理结果: {result}")
    
    print("\n验证码处理测试完成!")
    print(f"测试文件保存在: {captcha_dir}")
    print("请查看该目录下的文件，了解验证码处理的工作方式")


if __name__ == "__main__":
    test_captcha_handling()