# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


# useful for handling different item types with a single interface


class LianjiaHomeSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class LianjiaHomeDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    # 随机User-Agent列表
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    ]

    # 重试次数
    max_retry_times = 3

    # 重试间隔（秒）
    retry_delay = 5

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 设置随机User-Agent
        import random
        request.headers['User-Agent'] = random.choice(self.user_agents)

        # 添加随机延迟，避免请求过于频繁
        import time
        time.sleep(random.uniform(1, 3))

        # 添加一些常见请求头，模拟真实浏览器行为
        request.headers[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
        request.headers['Accept-Encoding'] = 'gzip, deflate, br, zstd'
        request.headers['Connection'] = 'keep-alive'
        request.headers['Upgrade-Insecure-Requests'] = '1'

        # 设置请求的dont_filter属性为False，避免重复请求
        request.dont_filter = False

        return None

    def process_response(self, request, response, spider):
        # 导入滑块验证码处理模块
        from slider_captcha import SliderCaptchaHandler
        # 检查是否遇到滑块验证码页面
        slider_handler = SliderCaptchaHandler(spider.settings if hasattr(spider, 'settings') else None)
        if slider_handler.is_slider_captcha(response):
            spider.logger.warning(f"遇到滑块验证码页面: {response.url}")

            # 记录重试次数
            retry_times = request.meta.get('retry_times', 0)

            if retry_times < self.max_retry_times:
                # 增加重试次数
                request.meta['retry_times'] = retry_times + 1

                # 尝试处理滑块验证码
                if slider_handler.handle_slider_captcha(response, request, spider):
                    spider.logger.info(f"滑块验证码处理成功: {response.url}")
                    # 验证码处理成功，重新发送请求
                    return request

                # 等待一段时间后重试
                import time
                time.sleep(self.retry_delay)

                # 更换User-Agent
                import random
                request.headers['User-Agent'] = random.choice(self.user_agents)

                # 返回新的请求对象，重新尝试
                spider.logger.info(f"重试请求 ({retry_times + 1}/{self.max_retry_times}): {request.url}")
                return request
            else:
                # 超过最大重试次数，记录错误
                spider.logger.error(f"滑块验证码验证失败，已达到最大重试次数: {request.url}")
                # 尝试最后一次手动处理
                slider_handler.handle_slider_captcha(response, request, spider)

        # 检查是否遇到普通验证码页面
        elif self._is_captcha_page(response):
            spider.logger.warning(f"遇到验证码页面: {response.url}")

            # 记录重试次数
            retry_times = request.meta.get('retry_times', 0)

            if retry_times < self.max_retry_times:
                # 增加重试次数
                request.meta['retry_times'] = retry_times + 1

                # 尝试自动处理验证码
                if self._handle_captcha(response, request, spider):
                    spider.logger.info(f"验证码自动处理成功: {response.url}")
                    # 验证码处理成功，重新发送请求
                    return request

                # 如果自动处理失败，尝试手动处理
                if self._handle_captcha_manually(response, request, spider):
                    spider.logger.info(f"验证码已手动处理: {response.url}")
                    # 手动处理后，重新发送请求
                    return request

                # 等待一段时间后重试
                import time
                time.sleep(self.retry_delay)

                # 更换User-Agent
                import random
                request.headers['User-Agent'] = random.choice(self.user_agents)

                # 返回新的请求对象，重新尝试
                spider.logger.info(f"重试请求 ({retry_times + 1}/{self.max_retry_times}): {request.url}")
                return request
            else:
                # 超过最大重试次数，记录错误
                spider.logger.error(f"验证码验证失败，已达到最大重试次数: {request.url}")
                # 尝试最后一次手动处理
                self._handle_captcha_manually(response, request, spider)

        return response

    def process_exception(self, request, exception, spider):
        # 处理请求异常，如连接超时、拒绝连接等
        spider.logger.error(f"请求异常: {request.url}, 异常: {exception}")

        # 记录重试次数
        retry_times = request.meta.get('retry_times', 0)

        if retry_times < self.max_retry_times:
            # 增加重试次数
            request.meta['retry_times'] = retry_times + 1

            # 等待一段时间后重试
            import time
            time.sleep(self.retry_delay)

            # 更换User-Agent
            import random
            request.headers['User-Agent'] = random.choice(self.user_agents)

            # 返回新的请求对象，重新尝试
            spider.logger.info(f"异常重试 ({retry_times + 1}/{self.max_retry_times}): {request.url}")
            return request

        return None

    def _is_captcha_page(self, response):
        """检查响应是否为验证码页面"""
        # 检查页面内容是否包含验证码相关的关键词或元素
        captcha_indicators = [
            '验证码',
            'captcha',
            'verify',
            '人机验证',
            '安全验证',
            '请输入验证码',
            '请完成验证',
            'sec_code',
            'security_check'
        ]

        # 检查状态码（通常验证码页面返回200，但内容是验证页面）
        if response.status == 200:
            # 检查页面内容
            page_text = response.text.lower()
            for indicator in captcha_indicators:
                if indicator.lower() in page_text:
                    return True

            # 检查是否有验证码图片元素
            captcha_selectors = [
                '//img[contains(@src, "captcha")]',
                '//img[contains(@src, "verify")]',
                '//div[contains(@class, "captcha")]',
                '//div[contains(@class, "verify")]',
                '//input[contains(@name, "captcha")]'
            ]

            for selector in captcha_selectors:
                if response.xpath(selector).get():
                    return True

        # 检查是否被重定向到验证页面
        if 'verify' in response.url or 'captcha' in response.url or 'security_check' in response.url:
            return True

        return False

    def _handle_captcha(self, response, request, spider):
        """处理验证码
        返回值: 布尔值，表示验证码是否处理成功
        """
        # 1. 尝试自动识别验证码
        try:
            # 查找验证码图片
            captcha_img_url = self._extract_captcha_image_url(response)
            if captcha_img_url:
                # 保存验证码图片
                import os
                import requests
                from datetime import datetime

                # 创建captcha目录（如果不存在）
                captcha_dir = os.path.join(os.getcwd(), 'captcha')
                if not os.path.exists(captcha_dir):
                    os.makedirs(captcha_dir)

                # 生成文件名
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                img_path = os.path.join(captcha_dir, f'captcha_{timestamp}.png')

                # 下载验证码图片
                img_response = requests.get(captcha_img_url, headers=request.headers)
                if img_response.status_code == 200:
                    with open(img_path, 'wb') as f:
                        f.write(img_response.content)
                    spider.logger.info(f"验证码图片已保存: {img_path}")

                    # 尝试使用第三方服务识别验证码
                    captcha_text = self._solve_captcha_with_service(img_path, spider)
                    if captcha_text:
                        # 提交验证码
                        success = self._submit_captcha(response, captcha_text, request, spider)
                        if success:
                            return True
        except Exception as e:
            spider.logger.error(f"自动处理验证码失败: {str(e)}")

        return False

    def _extract_captcha_image_url(self, response):
        """从响应中提取验证码图片URL"""
        # 尝试多种选择器查找验证码图片
        selectors = [
            '//img[contains(@src, "captcha")]/@src',
            '//img[contains(@src, "verify")]/@src',
            '//img[contains(@class, "captcha")]/@src',
            '//img[contains(@class, "verify")]/@src'
        ]

        for selector in selectors:
            img_url = response.xpath(selector).get()
            if img_url:
                # 如果是相对URL，转换为绝对URL
                if not img_url.startswith('http'):
                    from urllib.parse import urljoin
                    img_url = urljoin(response.url, img_url)
                return img_url

        return None

    def _solve_captcha_with_service(self, img_path, spider):
        """使用第三方服务识别验证码
        这里可以集成各种验证码识别服务，如2Captcha、Anti-Captcha等
        """
        # 示例：集成2Captcha服务（需要API密钥）
        try:
            # 这里需要安装并导入2captcha库
            # pip install 2captcha-python
            spider.logger.info("尝试使用第三方服务识别验证码")

            # 注意：实际使用时需要替换为你的API密钥
            # from twocaptcha import TwoCaptcha
            # solver = TwoCaptcha('YOUR_API_KEY')
            # result = solver.normal(img_path)
            # return result.get('code')

            # 由于没有实际的API密钥，这里返回None
            return None
        except Exception as e:
            spider.logger.error(f"验证码识别服务错误: {str(e)}")
            return None

    def _submit_captcha(self, response, captcha_text, request, spider):
        """提交验证码"""
        try:
            # 查找验证码表单
            form_selector = response.xpath('//form[.//input[contains(@name, "captcha")]]')
            if not form_selector:
                return False

            # 获取表单提交URL
            form_action = form_selector.xpath('@action').get()
            if not form_action:
                form_action = response.url
            else:
                from urllib.parse import urljoin
                form_action = urljoin(response.url, form_action)

            # 获取表单字段
            form_data = {}
            for input_field in form_selector.xpath('.//input'):
                name = input_field.xpath('@name').get()
                value = input_field.xpath('@value').get() or ''
                if name:
                    form_data[name] = value

            # 添加验证码值
            captcha_field_name = form_selector.xpath('.//input[contains(@name, "captcha")]/@name').get()
            if captcha_field_name:
                form_data[captcha_field_name] = captcha_text

            # 提交表单
            import requests
            headers = dict(request.headers)
            response = requests.post(form_action, data=form_data, headers=headers, cookies=request.cookies)

            # 检查是否成功（这里需要根据实际情况判断）
            if response.status_code == 200 and not self._is_captcha_page(response):
                return True
        except Exception as e:
            spider.logger.error(f"提交验证码失败: {str(e)}")

        return False

    def _handle_captcha_manually(self, response, request, spider):
        """手动处理验证码"""
        try:
            # 保存验证码页面，方便手动处理
            import os
            from datetime import datetime

            # 创建captcha目录（如果不存在）
            captcha_dir = os.path.join(os.getcwd(), 'captcha')
            if not os.path.exists(captcha_dir):
                os.makedirs(captcha_dir)

            # 生成文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            html_path = os.path.join(captcha_dir, f'captcha_page_{timestamp}.html')

            # 保存验证码页面
            with open(html_path, 'wb') as f:
                f.write(response.body)

            # 提取验证码图片并保存
            captcha_img_url = self._extract_captcha_image_url(response)
            if captcha_img_url:
                import requests
                img_path = os.path.join(captcha_dir, f'captcha_{timestamp}.png')

                # 下载验证码图片
                img_response = requests.get(captcha_img_url, headers=request.headers)
                if img_response.status_code == 200:
                    with open(img_path, 'wb') as f:
                        f.write(img_response.content)

                    # 创建一个说明文件，指导用户如何手动处理验证码
                    info_path = os.path.join(captcha_dir, f'captcha_info_{timestamp}.txt')
                    with open(info_path, 'w', encoding='utf-8') as f:
                        f.write(f"验证码页面URL: {response.url}\n")
                        f.write(f"验证码图片: {img_path}\n")
                        f.write(f"验证码页面HTML: {html_path}\n\n")
                        f.write("请手动处理验证码，步骤如下:\n")
                        f.write("1. 打开保存的HTML文件或直接访问上述URL\n")
                        f.write("2. 查看验证码图片并输入验证码\n")
                        f.write("3. 提交验证码后，将新的Cookie复制到爬虫配置中\n")

                    spider.logger.info(f"验证码需要手动处理，详情请查看: {info_path}")

                    # 暂停爬虫，等待手动处理
                    # 注意：这里只是示例，实际使用时可能需要更复杂的机制来暂停和恢复爬虫
                    import time
                    spider.logger.info("爬虫暂停30秒，等待手动处理验证码...")
                    time.sleep(30)  # 暂停30秒，给用户时间处理验证码

                    return True  # 返回True表示已处理（虽然可能需要用户手动操作）
        except Exception as e:
            spider.logger.error(f"手动处理验证码失败: {str(e)}")

        return False

    def spider_opened(self, spider):
        spider.logger.info('反爬虫中间件已启用: %s' % spider.name)
