# 单词数据库模型定义
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
import pymysql


# 数据库连接初始化
def get_db_connection():
    """
    获取数据库连接
    """
    # 建立数据库连接
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        db=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


# 初始化单词相关数据库表
def initialize_word_database():
    """初始化单词数据库表结构"""
    connection = get_db_connection()
    if not connection:
        return False

    try:
        with connection.cursor() as cursor:
            # 创建单词主表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS words (
                id INT AUTO_INCREMENT PRIMARY KEY,
                page_id INT NOT NULL,
                word_title VARCHAR(255) NOT NULL,
                meanings TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)

            # 创建单词发音表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS word_spells (
                id INT AUTO_INCREMENT PRIMARY KEY,
                word_id INT NOT NULL,
                spell VARCHAR(255) NOT NULL,
                audio VARCHAR(255)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)

            # 创建词性和释义表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS word_parts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                word_id INT NOT NULL,
                word_part VARCHAR(50) NOT NULL,
                word_part_meanings TEXT NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)

            # 创建单词详情表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS word_details (
                id INT AUTO_INCREMENT PRIMARY KEY,
                word_id INT NOT NULL,
                detail_key VARCHAR(255) NOT NULL,
                detail_value TEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)

            # 创建单词扩展用法表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS word_extensions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                word_id INT NOT NULL,
                ext_key VARCHAR(255) NOT NULL,
                ext_value TEXT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)

            # 创建同义词关系表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS word_thesaurus (
                id INT AUTO_INCREMENT PRIMARY KEY,
                word_id INT NOT NULL,
                thesaurus_word_id INT NOT NULL,
                thesaurus_title VARCHAR(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)

            # 创建反义词关系表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS word_antonyms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                word_id INT NOT NULL,
                antonym_word_id INT NOT NULL,
                antonym_title VARCHAR(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)

            # 创建同根词关系表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS word_conjugates (
                id INT AUTO_INCREMENT PRIMARY KEY,
                word_id INT NOT NULL,
                conjugate_word_id INT NOT NULL,
                conjugate_title VARCHAR(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)

        connection.commit()
        print("数据库表结构初始化成功")
        return True
    except Exception as e:
        print(f"初始化数据库表结构失败: {e}")
        return False
    finally:
        connection.close()


# 单词数据库管理类
class WordDatabaseManager:
    """
    单词数据库管理类，提供单词数据的存储和查询功能
    """

    @staticmethod
    def initialize_word_database():
        """
        初始化单词数据库表结构
        """
        try:
            initialize_word_database()
            return True
        except Exception as e:
            print(f"初始化单词数据库失败: {e}")
            return False

    @staticmethod
    def save_word(word_data):
        """保存单词数据到数据库"""
        connection = get_db_connection()
        if not connection:
            raise Exception("无法连接到数据库")

        try:
            with connection.cursor() as cursor:
                # 1. 保存单词基本信息
                cursor.execute("""
                INSERT INTO words (page_id, word_title, meanings) 
                VALUES (%s, %s, %s)
                """, (word_data['page_id'], word_data['word_tile'], word_data.get('meanings', '')))

                # 获取插入的单词ID
                word_id = connection.insert_id()

                # 2. 保存单词发音
                for spell in word_data.get('word_spells', []):
                    cursor.execute("""
                    INSERT INTO word_spells (word_id, spell, audio)
                    VALUES (%s, %s, %s)
                    """, (word_id, spell['spell'], spell.get('audio', '')))

                # 3. 保存词性和释义
                for part in word_data.get('word_detail', {}).get('word_parts', []):
                    cursor.execute("""
                    INSERT INTO word_parts (word_id, word_part, word_part_meanings)
                    VALUES (%s, %s, %s)
                    """, (word_id, part['word_part'], part['word_part_meanings']))

                # 4. 保存单词详情
                for key, value in word_data.get('word_detail', {}).items():
                    if key != 'word_parts':  # 词性和释义已单独保存
                        cursor.execute("""
                        INSERT INTO word_details (word_id, detail_key, detail_value)
                        VALUES (%s, %s, %s)
                        """, (word_id, key, value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)))

                # 5. 保存单词扩展用法
                for key, value in word_data.get('word_ext', {}).items():
                    cursor.execute("""
                    INSERT INTO word_extensions (word_id, ext_key, ext_value)
                    VALUES (%s, %s, %s)
                    """, (word_id, key, value))

                # 6. 保存同义词关系
                for thesaurus in word_data.get('thesaurus', []):
                    cursor.execute("""
                    INSERT INTO word_thesaurus (word_id, thesaurus_word_id, thesaurus_title)
                    VALUES (%s, %s, %s)
                    """, (word_id, thesaurus['id'], thesaurus['title']))

                # 7. 保存反义词关系
                for antonym in word_data.get('antonym', []):
                    cursor.execute("""
                    INSERT INTO word_antonyms (word_id, antonym_word_id, antonym_title)
                    VALUES (%s, %s, %s)
                    """, (word_id, antonym['id'], antonym['title']))

                # 8. 保存同根词关系
                for conjugate in word_data.get('conjugate', []):
                    cursor.execute("""
                    INSERT INTO word_conjugates (word_id, conjugate_word_id, conjugate_title)
                    VALUES (%s, %s, %s)
                    """, (word_id, conjugate['id'], conjugate['title']))

                connection.commit()
                return word_id
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

    @staticmethod
    def get_word_by_id(word_id):
        """
        通过ID获取单词完整信息

        参数:
            word_id: 单词ID

        返回:
            word_data: 包含单词完整信息的字典
        """
        conn = get_db_connection()
        try:
            word_data = {}

            with conn.cursor() as cursor:
                # 1. 获取单词基本信息
                cursor.execute("SELECT * FROM words WHERE id = %s", (word_id,))
                word = cursor.fetchone()
                if not word:
                    return None

                word_data['id'] = word['id']
                word_data['word'] = word['word']
                word_data['page_id'] = word['page_id']

                # 2. 获取单词发音信息
                cursor.execute("SELECT * FROM word_pronunciations WHERE word_id = %s", (word_id,))
                pronunciations = cursor.fetchall()
                word_data['pronunciations'] = pronunciations

                # 3. 获取单词词性和释义
                cursor.execute("SELECT * FROM word_parts WHERE word_id = %s", (word_id,))
                parts = cursor.fetchall()
                word_data['parts'] = parts

                # 4. 获取单词详细解释
                cursor.execute("SELECT * FROM word_details WHERE word_id = %s", (word_id,))
                details = cursor.fetchall()
                word_data['details'] = details

                # 5. 获取单词扩展用法
                cursor.execute("SELECT * FROM word_extensions WHERE word_id = %s", (word_id,))
                extensions = cursor.fetchall()
                word_data['extensions'] = extensions

                return word_data
        except Exception as e:
            print(f"获取单词数据失败: {e}")
            raise e
        finally:
            conn.close()

    @staticmethod
    def search_words(keyword, limit=20, offset=0):
        """
        搜索单词

        参数:
            keyword: 搜索关键词
            limit: 返回结果数量限制
            offset: 分页偏移量

        返回:
            words: 单词列表
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM words WHERE word LIKE %s LIMIT %s OFFSET %s",
                    (f"%{keyword}%", limit, offset)
                )
                return cursor.fetchall()
        except Exception as e:
            print(f"搜索单词失败: {e}")
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_word_master_view(word_id=None, keyword=None, limit=20, offset=0):
        """
        从单词总表视图获取单词完整信息

        参数:
            word_id: 单词ID，如果提供则精确查询该ID的单词
            keyword: 搜索关键词，如果提供则模糊查询包含该关键词的单词
            limit: 返回结果数量限制
            offset: 分页偏移量

        返回:
            words: 单词列表或单个单词信息
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                if word_id is not None:
                    # 精确查询单个单词
                    cursor.execute(
                        "SELECT * FROM word_master_view WHERE word_id = %s",
                        (word_id,)
                    )
                    return cursor.fetchone()
                elif keyword is not None:
                    # 模糊查询单词列表
                    cursor.execute(
                        "SELECT * FROM word_master_view WHERE word LIKE %s LIMIT %s OFFSET %s",
                        (f"%{keyword}%", limit, offset)
                    )
                    return cursor.fetchall()
                else:
                    # 获取所有单词列表
                    cursor.execute(
                        "SELECT * FROM word_master_view LIMIT %s OFFSET %s",
                        (limit, offset)
                    )
                    return cursor.fetchall()
        except Exception as e:
            print(f"从单词总表获取数据失败: {e}")
            raise e
        finally:
            conn.close()

    @staticmethod
    def parse_master_view_data(master_view_data):
        """
        解析单词总表视图数据为结构化字典

        参数:
            master_view_data: 从总表视图获取的单词数据

        返回:
            structured_data: 结构化的单词数据字典
        """
        if not master_view_data:
            return None

        result = {
            'id': master_view_data['word_id'],
            'word': master_view_data['word'],
            'page_id': master_view_data['page_id'],
            'created_at': master_view_data['created_at'],
            'updated_at': master_view_data['updated_at'],
            'pronunciations': [],
            'parts': [],
            'details': {},
            'extensions': {}
        }

        # 解析发音信息
        if master_view_data.get('pronunciations'):
            for pron in master_view_data['pronunciations'].split(';;'):
                if pron:
                    spell, audio = pron.split('|')
                    result['pronunciations'].append({
                        'spell': spell,
                        'audio_url': audio if audio else None
                    })

        # 解析词性和释义
        if master_view_data.get('parts_meanings'):
            for part_meaning in master_view_data['parts_meanings'].split(';;'):
                if part_meaning and ':' in part_meaning:
                    part, meanings = part_meaning.split(':', 1)
                    result['parts'].append({
                        'part': part,
                        'meanings': meanings
                    })

        # 解析详细解释
        if master_view_data.get('details'):
            for detail in master_view_data['details'].split(';;'):
                if detail and ':' in detail:
                    detail_type, content = detail.split(':', 1)
                    result['details'][detail_type] = content

        # 解析扩展用法
        if master_view_data.get('extensions'):
            for extension in master_view_data['extensions'].split(';;'):
                if extension and ':' in extension:
                    ext_type, content = extension.split(':', 1)
                    result['extensions'][ext_type] = content

        return result
