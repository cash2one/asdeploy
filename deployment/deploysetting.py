#coding:utf-8

import os

# 环境 参数(重要)
# 但页面右上角的env_logo不依赖这个变量，而取决于域名，页面模板不够强大
# 点击logo，可弹出此文件配置的真实的环境信息。
ENVIRONMENT = 'localhost'

# 版本
VERSION = '1.1'

# 数据库信息
DB_PARAMS = {
    'alpha': {
        'host': '192.168.150.7',
        'username': 'root',
        'password': 'mysqlpwd1',
    },
    'beta': {
        'host': '192.168.3.50',
        'username': 'root',
        'password': 'mysqlpwd1',
    },
    'localhost': {
        'host': '192.168.0.0',
        'username': 'root',
        'password': 'mysqlpwd1',
    },
}

DB_PARAM = DB_PARAMS[ENVIRONMENT]

# 服务器 信息，每个工程至少配置一个
WEB_SERVERS = {
    'alpha': {
        'as-web': ['web0.at1.ablesky.com'],
        'as-passport': ['passport0.at1.ablesky.com', 'passport1.at1.ablesky.com'],
        'as-search': ['se0.at1.ablesky.com'],
        'as-ad': ['ad0.at1.ablesky.com'],
        'as-im': ['im0.at1.ablesky.com'],
        'as-cms': ['cms0.at1.ablesky.com'],
    },
    'beta': {
        'as-web': ['web0.bt1.ablesky.com', 'web1.bt1.ablesky.com'],
        'as-passport': ['passport0.bt1.ablesky.com', 'passport1.bt1.ablesky.com'],
        'as-search': ['se0.bt1.ablesky.com', 'se1.bt1.ablesky.com'],
        'as-ad': ['ad0.bt1.ablesky.com'],
        'as-im': ['im0.bt1.ablesky.com', 'im1.bt1.ablesky.com'],
        'as-cms': ['cms0.bt1.ablesky.com'],
    },
    'localhost': {
        'as-web': ['web0.at1.ablesky.com'],
        'as-passport': ['passport0.at1.ablesky.com', 'passport1.at1.ablesky.com'],
        'as-search': ['se0.at1.ablesky.com'],
        'as-ad': ['ad0.at1.ablesky.com'],
        'as-im': ['im0.at1.ablesky.com'],
        'as-cms': ['cms0.at1.ablesky.com'],
    },
}

WEB_SERVER = WEB_SERVERS[ENVIRONMENT]

# 发布超时解锁时间(秒)，调用 _check_lock()的时候会去判断超时和解锁
LOCK_TIMEOUT_PERIOD = 3600 * 1.5

# 发布后是否发邮件
NEED_SEND_EMAIL = False

# 目录

FOLDER_ROOT = '/v/content/web-app-bak/'

ITEM_ROOT_PATH = FOLDER_ROOT + 'ableskyapps/'

SHELL_ROOT_PATH = FOLDER_ROOT + 'deployment/'

DEPLOY_LOG_NAME = 'deploy.log'

DEPLOY_LOG_PATH = SHELL_ROOT_PATH + DEPLOY_LOG_NAME

# 文件上传的临时目录
DPL_FILE_UPLOAD_TEMP_DIR = '/v/content/web-app-bak/ableskyapps/tempuploads/'


# ftp运行目录

FTP_APACHE_PATH = '/usr/share/apache-tomcat-7.0.11/ableskyapps/'

FTP_LOCAL_DOWNLOAD_FILE_PATH = os.path.join(os.path.dirname(__file__), './download_file_folder/')

FTP_LOCAL_TEMP_FILE_PATH = os.path.join(os.path.dirname(__file__), './temp_file_folder/')

FTP_PORT = 22

FTP_USERNAME = 'root'

FTP_PASSWORD = 'ASdiyi'

