import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库连接地址
MYSQL_URL = 'mysql://blog:123456@192.168.1.214:3306/blog?charset=utf8'

# 运行日志
RUN_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'run.log')


# 七牛配置
