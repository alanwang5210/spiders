# 链家二手房数据爬虫

这是一个使用Scrapy框架开发的链家二手房数据爬虫项目，用于爬取链家网站上的二手房信息。

## 功能特点

- 爬取链家二手房基本信息（名称、户型、面积、朝向、装修情况等）
- 爬取房屋详细信息（产权信息、电梯配备等）
- 实现了反爬虫机制应对措施
  - 随机User-Agent
  - 请求延迟和并发控制
  - 验证码检测和处理
  - 异常重试机制

## 项目结构

```
lianjia_home/
  ├── lianjia_home/
  │   ├── __init__.py
  │   ├── items.py          # 数据项定义
  │   ├── middlewares.py    # 中间件（包含反爬虫处理）
  │   ├── pipelines.py      # 数据处理管道
  │   ├── settings.py       # 项目设置
  │   └── spiders/
  │       ├── __init__.py
  │       └── home.py       # 爬虫主程序
  └── scrapy.cfg            # Scrapy配置文件
```

## 安装

```bash
# 克隆项目
git clone <repository-url>
cd lianjia_home

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

```bash
# 运行爬虫
scarpy crawl home

# 将结果保存为CSV文件
scarpy crawl home -o houses.csv
```

## 验证码处理

本项目实现了基本的验证码检测和处理机制：

1. **自动检测验证码页面**：中间件会自动检测是否遇到验证码页面
2. **自动重试**：遇到验证码时会自动等待一段时间并更换User-Agent后重试
3. **重试限制**：设置了最大重试次数，避免无限循环

### 手动处理验证码

如果自动重试无法解决验证码问题，可以考虑以下方法：

1. **使用代理IP**：在middlewares.py中添加代理IP池，定期更换IP地址
2. **降低爬取频率**：在settings.py中增加DOWNLOAD_DELAY的值
3. **手动登录获取Cookie**：
   - 手动在浏览器中登录链家网站
   - 获取Cookie并在爬虫中使用
   - 在home.py的start_requests方法中设置Cookie

## 注意事项

- 本项目仅用于学习和研究，请勿用于商业用途
- 请遵守网站的robots.txt规则
- 爬取数据时请控制频率，避免对目标网站造成压力