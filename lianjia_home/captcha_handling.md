# 链家爬虫验证码处理指南

本文档提供了处理链家网站验证码的详细说明，包括普通验证码和滑块验证码的处理方法。

## 验证码处理机制

当爬虫遇到验证码时，会按照以下步骤处理：

1. 首先检测验证码类型（普通验证码或滑块验证码）
2. 根据验证码类型选择相应的处理方法
3. 尝试自动处理验证码（如果启用）
4. 如果自动处理失败，则尝试手动处理（如果启用）
5. 如果以上都失败，则等待一段时间后重试
6. 如果重试次数超过最大限制，则记录错误并停止

## 普通验证码处理

### 配置第三方验证码识别服务

1. 在 `settings.py` 中设置：
   ```python
   CAPTCHA_ENABLED = True
   CAPTCHA_API_KEY = "your_api_key_here"  # 替换为你的API密钥
   CAPTCHA_SERVICE = "2captcha"  # 支持：2captcha, anticaptcha 等
   ```

2. 安装相应的依赖：
   ```bash
   pip install 2captcha-python  # 如果使用2Captcha服务
   # 或
   pip install anticaptchaofficial  # 如果使用Anti-Captcha服务
   ```

## 滑块验证码处理

### 配置自动滑块验证码处理

1. 在 `settings.py` 中设置：
   ```python
   SLIDER_CAPTCHA_AUTO_ENABLED = True
   SLIDER_CAPTCHA_USE_SELENIUM = True  # 使用Selenium处理滑块验证码
   # 或
   SLIDER_CAPTCHA_USE_PLAYWRIGHT = True  # 使用Playwright处理滑块验证码
   ```

2. 安装相应的依赖：
   ```bash
   # 如果使用Selenium
   pip install selenium webdriver-manager
   
   # 如果使用Playwright
   pip install playwright
   playwright install
   
   # 图像处理相关依赖
   pip install opencv-python numpy
   ```

## 手动验证码处理

当自动验证码处理失败时，爬虫会：

1. 保存验证码页面HTML和验证码图片到 `captcha` 目录
2. 创建一个说明文件，指导如何手动处理验证码
3. 暂停爬虫一段时间，等待手动处理

### 手动处理步骤

1. 打开保存的HTML文件或直接访问验证码页面URL
2. 查看验证码图片并输入验证码
3. 提交验证码后，将新的Cookie复制到爬虫配置中

### 更新Cookie

成功处理验证码后，你需要更新爬虫的Cookie：

1. 在浏览器中复制新的Cookie
2. 更新 `home.py` 中的 `cookie_str` 变量

## 优化建议

为减少触发验证码的频率：

1. 降低请求频率（增加 `DOWNLOAD_DELAY`）
2. 减少并发请求数（降低 `CONCURRENT_REQUESTS_PER_DOMAIN` 和 `CONCURRENT_REQUESTS_PER_IP`）
3. 使用代理IP轮换（可以考虑添加代理中间件）
4. 模拟更真实的浏览器行为（已在中间件中实现）

## 故障排除

如果验证码处理持续失败：

1. 检查网络连接是否稳定
2. 验证第三方服务API密钥是否有效
3. 尝试使用不同的浏览器手动访问网站，确认是否有其他反爬措施
4. 考虑增加更长的等待时间或使用代理IP