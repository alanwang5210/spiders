import os
import random
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from word_models import WordDatabaseManager


class XinDongFangSpiderWithDB:
    """新东方单词爬虫类 - 带数据库存储功能"""

    def __init__(self, init_db=False, base_url="https://www.koolearn.com/dict"):
        """初始化爬虫"""
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.koolearn.com/dict/'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.data_dir = "koolearn_data"

        # 创建数据存储目录
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # 初始化数据库
        if init_db:
            self.db_initialized = WordDatabaseManager.initialize_word_database()
            if not self.db_initialized:
                print("警告: 数据库初始化失败，数据将不会被保存到数据库")

    def get_page(self, url, retry=3):
        """获取页面内容"""
        for i in range(retry):
            try:
                # 添加随机延迟，避免请求过于频繁
                time.sleep(random.uniform(1, 3))
                response = self.session.get(url, timeout=10)
                response.raise_for_status()  # 如果状态码不是200，则抛出异常
                response.encoding = 'utf-8'  # 确保中文正确编码
                return response.text
            except Exception as e:
                print(f"获取页面失败: {url}, 错误: {e}, 重试次数: {i + 1}/{retry}")
                if i == retry - 1:
                    return None
        return None

    def crawl_with_details(self, start_page=1, end_page=2, save_to_db=True):
        """爬取单词详情并保存到数据库"""
        saved_words = []
        failed_words = []

        for page in range(start_page, end_page + 1):
            """爬取单词"""
            url = f"{self.base_url}/wd_{page}.html"
            print(f"正在爬取第 {page} 个单词...")

            html = self.get_page(url)

            """解析单词列表页面"""
            if not html:
                print(f"获取页面 {url} 失败，跳过")
                continue

            soup = BeautifulSoup(html, 'html.parser')

            try:
                # 根据网页结构查找单词列表
                word_elem = soup.select_one('div.left-content')
                if not word_elem:
                    print(f"在页面 {url} 中未找到单词内容，跳过")
                    continue

                word = {'page_id': page}

                word_tile = word_elem.select_one('div.word-title, div.word-spell').text.strip()
                word['word_tile'] = word_tile

                word_spells = []
                word_spells_elem = word_elem.select('div.word-spell-box')
                for word_spell_elem in word_spells_elem:
                    word_spell = {'spell': word_spell_elem.select_one("span.word-spell").text.strip(),
                                  'audio': word_spell_elem.select_one("span.word-spell-audio").get('data-url')}
                    word_spells.append(word_spell)
                word['word_spells'] = word_spells

                word_detail = {}
                word_ext = {}
                word_parts = []
                meaning_str = ''
                word_parts_elems = word_elem.select('div.details-content-title-box li.clearfix')
                for word_part_elems in word_parts_elems:
                    word_part = word_part_elems.select_one('span.prop').text.strip()
                    word_part_meanings = word_part_elems.select_one('p').text.strip()
                    meaning_str = meaning_str + word_part_meanings
                    word_parts.append({'word_part': word_part, 'word_part_meanings': word_part_meanings})

                word['meanings'] = meaning_str
                word_detail['word_parts'] = word_parts

                word_detail_elems = word_elem.select('div.details-content-title-box')
                for word_detail_elem in word_detail_elems:
                    if word_detail_elem.find_parent().find_previous().text.strip() == '是什么意思':
                        # 找到所有的 h2 标签
                        word_detail_tags_elem = word_detail_elem.find_all('h2')
                        for word_detail_tag_elem in word_detail_tags_elem:
                            # 获取 h2 标签的文本内容，作为字典的键
                            key = word_detail_tag_elem.get_text()
                            # 找到 h2 标签的下一个兄弟 div 标签
                            word_detail_value_elem = word_detail_tag_elem.find_next_sibling('div')
                            if word_detail_value_elem:
                                # 获取 div 标签的文本内容，作为字典的值
                                value = word_detail_value_elem.get_text()
                                # 将键值对添加到字典中
                                word_detail[key] = value
                    elif word_detail_elem.find_parent().find_previous().text.strip() == '学习怎么用':
                        # 找到所有的 h2 标签
                        word_detail_tags_elem = word_detail_elem.find_all('h2')
                        for word_detail_tag_elem in word_detail_tags_elem:
                            # 获取 h2 标签的文本内容，作为字典的键
                            key = word_detail_tag_elem.get_text()
                            # 找到 h2 标签的下一个兄弟 div 标签
                            word_detail_value_elem = word_detail_tag_elem.find_next_sibling('div')
                            if word_detail_value_elem:
                                # 获取 div 标签的文本内容，作为字典的值
                                value = word_detail_value_elem.get_text()
                                # 将键值对添加到字典中
                                word_ext[key] = value
                word['word_detail'] = word_detail
                word['word_ext'] = word_ext

                word_thesaurus = []
                word_antonym = []
                word_conjugate = []
                word_relation_elems = soup.select('div.right-content div.retrieve-title')

                for word_relation_elem in word_relation_elems:
                    if word_relation_elem.text.strip() == '同义词':

                        word_thesaurus_a_s = word_relation_elem.find_next('div').select('a')
                        for word_thesaurus_a in word_thesaurus_a_s:
                            word_thesaurus_dict = {}
                            path = Path(word_thesaurus_a.get('href'))
                            # 获取文件名（不包含扩展名）
                            stem = path.stem
                            # 按 '_' 分割文件名，取第二部分
                            word_thesaurus_dict['id'] = stem.split('_')[-1]
                            word_thesaurus_dict['title'] = word_thesaurus_a.text.strip()
                            word_thesaurus.append(word_thesaurus_dict)

                    elif word_relation_elem.text.strip() == '反义词':

                        word_antonym_a_s = word_relation_elem.find_next('div').select('a')
                        for word_antonym_a in word_antonym_a_s:
                            word_antonym_dict = {}
                            path = Path(word_antonym_a.get('href'))
                            # 获取文件名（不包含扩展名）
                            stem = path.stem
                            # 按 '_' 分割文件名，取第二部分
                            word_antonym_dict['id'] = stem.split('_')[-1]
                            word_antonym_dict['title'] = word_antonym_a.text.strip()
                            word_antonym.append(word_antonym_dict)

                    elif word_relation_elem.text.strip() == '同根词':

                        word_conjugate_a_s = word_relation_elem.find_next('div').select('a')
                        for word_conjugate_a in word_conjugate_a_s:
                            word_conjugate_dict = {}
                            path = Path(word_conjugate_a.get('href'))
                            # 获取文件名（不包含扩展名）
                            stem = path.stem
                            # 按 '_' 分割文件名，取第二部分
                            word_conjugate_dict['id'] = stem.split('_')[-1]
                            word_conjugate_dict['title'] = word_conjugate_a.text.strip()
                            word_conjugate.append(word_conjugate_dict)

                word['thesaurus'] = word_thesaurus
                word['antonym'] = word_antonym
                word['conjugate'] = word_conjugate

                print(f"成功解析单词: {word['word_tile']}")

                # 保存到数据库
                if save_to_db:
                    try:
                        word_id = WordDatabaseManager.save_word(word)
                        print(f"单词 '{word['word_tile']}' 已保存到数据库，ID: {word_id}")
                        saved_words.append({'word': word['word_tile'], 'id': word_id})
                    except Exception as db_error:
                        print(f"保存单词 '{word['word_tile']}' 到数据库失败: {db_error}")
                        failed_words.append({'word': word['word_tile'], 'error': str(db_error)})

            except Exception as e:
                print(f"解析单词条目时出错: {e}")
                failed_words.append({'page_id': page, 'error': str(e)})

            # 每页爬取完后休息一下，避免请求过于频繁
            if page < end_page:
                sleep_time = random.uniform(1, 3)
                print(f"第 {page} 页爬取完成，休息 {sleep_time:.2f} 秒后继续爬取下一页...")
                time.sleep(sleep_time)

        # 打印爬取结果统计
        print("\n爬取完成！")
        print(f"成功保存到数据库的单词数量: {len(saved_words)}")
        print(f"保存失败的单词数量: {len(failed_words)}")

        return saved_words, failed_words


if __name__ == "__main__":
    # 创建爬虫实例
    spider = XinDongFangSpiderWithDB(init_db=True)

    # 爬取单词并保存到数据库
    spider.crawl_with_details(start_page=47376, end_page=168485, save_to_db=True)
