# -*- coding: utf-8 -*-
# 滑块验证码处理模块

import os
import time
import random
import base64
import logging
from urllib.parse import urljoin
from datetime import datetime

# 日志配置
logger = logging.getLogger(__name__)

class SliderCaptchaHandler:
    """滑块验证码处理类"""
    
    def __init__(self, settings=None):
        """初始化滑块验证码处理器
        
        Args:
            settings: Scrapy设置对象
        """
        self.settings = settings or {}
        self.captcha_dir = self.settings.get('SLIDER_CAPTCHA_DIR', 'captcha')
        self.manual_wait_time = self.settings.get('SLIDER_CAPTCHA_MANUAL_WAIT_TIME', 30)
        self.auto_enabled = self.settings.get('SLIDER_CAPTCHA_AUTO_ENABLED', False)
        
        # 确保验证码目录存在
        if not os.path.exists(self.captcha_dir):
            os.makedirs(self.captcha_dir)
    
    def is_slider_captcha(self, response):
        """检查是否为滑块验证码页面
        
        Args:
            response: Scrapy响应对象
            
        Returns:
            bool: 是否为滑块验证码页面
        """
        # 检查页面内容是否包含滑块验证码相关的关键词或元素
        slider_indicators = [
            '请拖动滑块',
            '拖动滑块完成拼图',
            '请完成安全验证',
            'slide to verify',
            'slider captcha',
            '滑动验证',
            '滑块验证',
            '拖动滑块验证'
        ]
        
        # 检查页面内容
        page_text = response.text.lower()
        for indicator in slider_indicators:
            if indicator.lower() in page_text:
                return True
        
        # 检查是否有滑块验证码相关元素
        slider_selectors = [
            '//div[contains(@class, "slider")]',
            '//div[contains(@class, "captcha-slider")]',
            '//div[contains(@class, "slide-verify")]',
            '//div[contains(@class, "verify-slider")]',
            '//div[contains(@id, "slider")]',
            '//div[contains(@id, "captcha-slider")]'
        ]
        
        for selector in slider_selectors:
            if response.xpath(selector).get():
                return True
        
        return False
    
    def handle_slider_captcha(self, response, request, spider):
        """处理滑块验证码
        
        Args:
            response: Scrapy响应对象
            request: Scrapy请求对象
            spider: Scrapy爬虫对象
            
        Returns:
            bool: 验证码是否处理成功
        """
        try:
            # 记录遇到滑块验证码
            spider.logger.warning(f"遇到滑块验证码: {response.url}")
            
            # 保存验证码页面，方便分析
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            html_path = os.path.join(self.captcha_dir, f'slider_captcha_page_{timestamp}.html')
            
            with open(html_path, 'wb') as f:
                f.write(response.body)
            
            # 尝试自动处理滑块验证码
            if self.auto_enabled:
                if self._auto_solve_slider(response, request, spider):
                    spider.logger.info(f"滑块验证码自动处理成功: {response.url}")
                    return True
            
            # 自动处理失败或未启用，尝试手动处理
            if self._handle_slider_manually(response, request, spider):
                spider.logger.info(f"滑块验证码已手动处理: {response.url}")
                return True
            
            return False
        except Exception as e:
            spider.logger.error(f"处理滑块验证码失败: {str(e)}")
            return False
    
    def _auto_solve_slider(self, response, request, spider):
        """自动解决滑块验证码
        
        Args:
            response: Scrapy响应对象
            request: Scrapy请求对象
            spider: Scrapy爬虫对象
            
        Returns:
            bool: 是否成功解决
        """
        try:
            # 这里需要实现自动解决滑块验证码的逻辑
            # 通常需要使用Selenium或Playwright等浏览器自动化工具
            # 由于需要额外的依赖，这里只提供基本框架
            
            spider.logger.info("尝试自动解决滑块验证码...")
            
            # 示例：使用Selenium处理滑块验证码
            # 注意：实际使用时需要安装selenium并配置webdriver
            # from selenium import webdriver
            # from selenium.webdriver.common.by import By
            # from selenium.webdriver.common.action_chains import ActionChains
            # 
            # # 创建浏览器实例
            # driver = webdriver.Chrome()
            # driver.get(response.url)
            # 
            # # 等待滑块元素加载
            # slider = driver.find_element(By.XPATH, '//div[contains(@class, "slider")]')
            # 
            # # 获取滑块和背景图片
            # slider_img = driver.find_element(By.XPATH, '//img[contains(@class, "slider-img")]')
            # bg_img = driver.find_element(By.XPATH, '//img[contains(@class, "bg-img")]')
            # 
            # # 计算滑动距离（这需要图像处理算法来确定）
            # distance = self._calculate_slider_distance(slider_img, bg_img)
            # 
            # # 模拟人类滑动行为
            # action = ActionChains(driver)
            # action.click_and_hold(slider)
            # action.move_by_offset(distance, 0)
            # action.release()
            # action.perform()
            # 
            # # 等待验证结果
            # time.sleep(2)
            # 
            # # 获取新的cookies
            # cookies = driver.get_cookies()
            # 
            # # 更新请求的cookies
            # for cookie in cookies:
            #     request.cookies[cookie['name']] = cookie['value']
            # 
            # # 关闭浏览器
            # driver.quit()
            # 
            # return True
            
            # 当前未实现自动处理，返回False
            return False
        except Exception as e:
            spider.logger.error(f"自动解决滑块验证码失败: {str(e)}")
            return False
    
    def _calculate_slider_distance(self, slider_img, bg_img):
        """计算滑块需要滑动的距离
        
        Args:
            slider_img: 滑块图片
            bg_img: 背景图片
            
        Returns:
            int: 滑动距离（像素）
        """
        # 这里需要实现图像处理算法来计算滑动距离
        # 通常涉及到图像处理库如OpenCV
        # 
        # 示例算法流程：
        # 1. 将滑块图片和背景图片转换为灰度图
        # 2. 对图片进行边缘检测
        # 3. 使用模板匹配找到滑块在背景图中的位置
        # 4. 返回匹配位置的x坐标
        
        # 由于需要额外的依赖，这里只返回一个随机值作为示例
        return random.randint(50, 200)
    
    def _simulate_human_slide(self, distance):
        """模拟人类滑动轨迹
        
        Args:
            distance: 总滑动距离
            
        Returns:
            list: 滑动轨迹列表，每个元素为(x, y, t)，表示x方向移动距离、y方向移动距离和时间
        """
        # 生成符合人类行为特征的滑动轨迹
        # 通常包括：初始慢速、中间加速、结尾减速、微小的Y轴抖动
        
        tracks = []
        # 当前的滑动总距离
        current = 0
        # 减速阈值，当滑动距离达到总距离的mid_point比例时开始减速
        mid_point = random.uniform(0.6, 0.8)
        # 时间间隔
        t = 0.2
        # 初始速度
        v = 0
        
        while current < distance:
            # 加速度，模拟人类滑动特性
            if current / distance < mid_point:
                # 加速阶段
                a = random.uniform(2, 5)
            else:
                # 减速阶段
                a = random.uniform(-3, -1)
            
            # 计算当前速度
            v0 = v
            v = v0 + a * t
            # 防止速度为负
            v = max(0, v)
            
            # 计算移动距离
            move = v * t + 0.5 * a * t * t
            # 防止超过目标距离
            move = min(move, distance - current)
            
            # 添加轨迹点，包含微小的Y轴抖动
            y_offset = random.uniform(-2, 2)
            tracks.append((move, y_offset, t))
            
            # 更新当前距离
            current += move
        
        return tracks
    
    def _handle_slider_manually(self, response, request, spider):
        """手动处理滑块验证码
        
        Args:
            response: Scrapy响应对象
            request: Scrapy请求对象
            spider: Scrapy爬虫对象
            
        Returns:
            bool: 是否成功处理
        """
        try:
            # 保存验证码页面，方便手动处理
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            html_path = os.path.join(self.captcha_dir, f'slider_captcha_page_{timestamp}.html')
            
            # 保存验证码页面
            with open(html_path, 'wb') as f:
                f.write(response.body)
            
            # 创建一个说明文件，指导用户如何手动处理滑块验证码
            info_path = os.path.join(self.captcha_dir, f'slider_captcha_info_{timestamp}.txt')
            with open(info_path, 'w', encoding='utf-8') as f:
                f.write(f"滑块验证码页面URL: {response.url}\n")
                f.write(f"验证码页面HTML: {html_path}\n\n")
                f.write("请手动处理滑块验证码，步骤如下:\n")
                f.write("1. 打开保存的HTML文件或直接访问上述URL\n")
                f.write("2. 完成滑块验证\n")
                f.write("3. 验证成功后，将新的Cookie复制到爬虫配置中\n")
            
            spider.logger.info(f"滑块验证码需要手动处理，详情请查看: {info_path}")
            
            # 暂停爬虫，等待手动处理
            spider.logger.info(f"爬虫暂停{self.manual_wait_time}秒，等待手动处理滑块验证码...")
            time.sleep(self.manual_wait_time)
            
            return True  # 返回True表示已处理（虽然可能需要用户手动操作）
        except Exception as e:
            spider.logger.error(f"手动处理滑块验证码失败: {str(e)}")
            return False