# -*- coding: utf-8 -*-
# 滑块验证码处理测试脚本

import os
import sys
import requests
from urllib.parse import urljoin
from datetime import datetime

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入爬虫相关模块
from lianjia_home.slider_captcha import SliderCaptchaHandler


def test_slider_captcha_handling():
    """测试滑块验证码处理功能"""
    print("开始测试滑块验证码处理功能...")
    
    # 创建滑块验证码处理器实例
    settings = {
        'SLIDER_CAPTCHA_DIR': 'captcha',
        'SLIDER_CAPTCHA_MANUAL_WAIT_TIME': 10,  # 为了测试方便，设置较短的等待时间
        'SLIDER_CAPTCHA_AUTO_ENABLED': False
    }
    slider_handler = SliderCaptchaHandler(settings)
    
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
            if '//div[contains(@class, "slider")]' in selector:
                return MockSelector(True)
            return MockSelector(False)
    
    class MockSelector:
        def __init__(self, has_result=False):
            self.has_result = has_result
            
        def get(self):
            # 模拟返回滑块元素
            if self.has_result:
                return "<div class='slider'></div>"
            return None
    
    # 创建测试目录
    captcha_dir = os.path.join(os.getcwd(), 'captcha')
    if not os.path.exists(captcha_dir):
        os.makedirs(captcha_dir)
    
    # 创建模拟滑块验证码页面HTML
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    html_path = os.path.join(captcha_dir, f'test_slider_captcha_page_{timestamp}.html')
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>滑块验证码测试页面</title>
        <style>
            .slider-container {{width: 300px; height: 40px; background-color: #f0f0f0; position: relative; margin: 50px auto;}}
            .slider {{width: 40px; height: 40px; background-color: #3498db; position: absolute; cursor: pointer;}}
            .slider-bg {{width: 300px; height: 200px; background-color: #e0e0e0; margin: 20px auto;}}
            .slider-block {{width: 40px; height: 40px; background-color: #ffffff; position: absolute; top: 80px; left: 100px;}}
        </style>
    </head>
    <body>
        <h1>请拖动滑块完成拼图</h1>
        <div class="slider-bg">
            <div class="slider-block"></div>
        </div>
        <div class="slider-container">
            <div class="slider"></div>
        </div>
    </body>
    </html>
    '''
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 创建模拟响应对象
    mock_response = MockResponse(
        url="https://su.lianjia.com/verify/slider",
        body=html_content.encode('utf-8')
    )
    
    # 创建模拟请求对象
    mock_request = MockRequest(url="https://su.lianjia.com/ershoufang/")
    
    # 创建模拟爬虫对象
    mock_spider = MockSpider()
    
    # 测试滑块验证码检测
    print("\n测试滑块验证码页面检测...")
    is_slider_captcha = slider_handler.is_slider_captcha(mock_response)
    print(f"是否为滑块验证码页面: {is_slider_captcha}")
    
    # 测试滑块验证码处理
    if is_slider_captcha:
        print("\n测试滑块验证码处理...")
        # 测试自动处理（当前未实现，预期会失败）
        settings['SLIDER_CAPTCHA_AUTO_ENABLED'] = True
        slider_handler = SliderCaptchaHandler(settings)
        result = slider_handler._auto_solve_slider(mock_response, mock_request, mock_spider)
        print(f"自动处理结果: {result}")
        
        # 测试手动处理
        print("\n测试手动处理滑块验证码...")
        settings['SLIDER_CAPTCHA_AUTO_ENABLED'] = False
        slider_handler = SliderCaptchaHandler(settings)
        result = slider_handler._handle_slider_manually(mock_response, mock_request, mock_spider)
        print(f"手动处理结果: {result}")
    
    print("\n滑块验证码处理测试完成!")
    print(f"测试文件保存在: {captcha_dir}")
    print("请查看该目录下的文件，了解滑块验证码处理的工作方式")


if __name__ == "__main__":
    test_slider_captcha_handling()