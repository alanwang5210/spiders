# Scrapy settings for lianjia_home project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "lianjia_home"

SPIDER_MODULES = ["lianjia_home.spiders"]
NEWSPIDER_MODULE = "lianjia_home.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "lianjia_home (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 2
CONCURRENT_REQUESTS_PER_IP = 2

# Disable cookies (enabled by default)
COOKIES_ENABLED = True  # 链家网站可能需要cookie来维持会话

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "lianjia_home.middlewares.LianjiaHomeSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "lianjia_home.middlewares.LianjiaHomeDownloaderMiddleware": 543,
#    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,  # 禁用默认的重试中间件，使用我们自定义的重试逻辑
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "lianjia_home.pipelines.LianjiaHomePipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# 验证码处理相关设置
# 是否启用自动验证码处理
CAPTCHA_ENABLED = True
# 是否启用手动验证码处理（当自动处理失败时）
CAPTCHA_MANUAL_ENABLED = True
# 验证码识别服务API密钥（如果使用第三方服务）
# CAPTCHA_API_KEY = "your_api_key_here"
# 验证码识别服务类型（支持：2captcha, anticaptcha, 等）
CAPTCHA_SERVICE = "2captcha"
# 验证码文件保存目录
CAPTCHA_DIR = "captcha"
# 手动处理验证码时的等待时间（秒）
CAPTCHA_MANUAL_WAIT_TIME = 30

# 滑块验证码处理相关设置
# 是否启用自动滑块验证码处理
SLIDER_CAPTCHA_AUTO_ENABLED = False
# 滑块验证码文件保存目录
SLIDER_CAPTCHA_DIR = "captcha"
# 手动处理滑块验证码时的等待时间（秒）
SLIDER_CAPTCHA_MANUAL_WAIT_TIME = 60
# 是否使用Selenium处理滑块验证码
SLIDER_CAPTCHA_USE_SELENIUM = False
# 是否使用Playwright处理滑块验证码
SLIDER_CAPTCHA_USE_PLAYWRIGHT = False
