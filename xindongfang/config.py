# 主配置文件
import os
import yaml


# 加载YAML配置文件
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if not os.path.exists(config_path):
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml.example')

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# 加载配置
config = load_config()

# 数据库配置
DB_HOST = config['database']['host']
DB_PORT = config['database']['port']
DB_USER = config['database']['user']
DB_PASSWORD = config['database']['password']
DB_NAME = config['database']['name']
