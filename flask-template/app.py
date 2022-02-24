import sys
sys.path.append(".")
import os
from os import path
from datetime import timedelta

from nanoid import generate
import pymysql
from flask import Flask, flash, request, redirect, current_app, session
from dbutils.pooled_db import PooledDB
from werkzeug.utils import secure_filename

from utils.wrappers import *

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # 配置session
        SESSION_KEY = "",
        PERMANENT_SESSION_LIFETIME = timedelta(days=7),
        # 配置数据库连接池
        PYMYSQL_POOL = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,
            # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            ping=0,
            host='bj-cynosdbmysql-grp-2r0nnbpu.sql.tencentcdb.com',
            port=22241,
            user='tmp',
            password='Aa1@0000',
            database='demo',#链接的数据库的名字
            charset='utf8'
        ),
        # 配置原生文件上传, 覆盖
        UPLOAD_FOLDER = path.join(path.dirname(path.abspath(__file__)), "static/avatar"),  # 上传目录
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}, # 允许上传的文件类型
        MAX_CONTENT_LENGTH = 16 * 1000 * 1000,  # 最大文件大小 16M
        # flask_uploads文件上传, 若存在则加后缀
        UPLOADED_PHOTOS_DEST = path.join(path.dirname(path.abspath(__file__)), "uploads"),
        UPLOADED_FILES_ALLOW = ['apk', 'zip', 'jpg'],  # 配置允许的扩展名，其他的都是不允许,
        UPLOADED_FILES_DENY = ['html'], # 配置不允许的扩展名
    )
    
    configure_folders(app)
    configure_handler(app)
    configure_views(app)
    configure_cross(app)
    return app


def configure_folders(app):
    # 配置上传文件夹
    from flask_uploads import UploadSet, configure_uploads, IMAGES
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, [photos])

def configure_views(app):
    # 配置视图文件夹
    from views import account as views_account
    from views import article as views_article
    from views import sentence as views_sentence
    from views import megazine as views_megazine
    app.register_blueprint(views_account.account)
    app.register_blueprint(views_article.article)
    app.register_blueprint(views_sentence.sentence)
    app.register_blueprint(views_megazine.megazine)

def configure_handler(app):

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST' and 'photo' in request.files:
            file = request.files['photo']
            filename = secure_filename(file.filename)
            filename = photos.save(request.files['photo'], name=generate(size=30) + '.' + filename.split(".")[-1])
            flash("Photo saved.")
        return {}

    @app.route('/nanoid')
    @is_login
    def nanoid(n = 10):
        return generate(size=n)

def configure_cross(app):
    @app.after_request
    def cors(environ):
        environ.headers['Access-Control-Allow-Origin']='*'
        environ.headers['Access-Control-Allow-Method']='*'
        environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
        return environ

if __name__ == '__main__':
    app = create_app()
    app.run()