import sys
sys.path.append(".")
import os
import time
from os import path
from datetime import timedelta

from nanoid import generate
import pymysql
from flask import jsonify, Flask, flash, request, redirect, current_app, session
from dbutils.pooled_db import PooledDB
from werkzeug.utils import secure_filename

from nanoid import generate
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, session, redirect, current_app, flash, url_for

from utils.db import SQLHelper
from utils.tokenUtil import TokenHelper
from utils.wrappers import *


IS_SERVERLESS = bool(os.environ.get('SERVERLESS'))
print(IS_SERVERLESS)

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
    account(app)
    article(app)
    sentence(app)
    megazine(app)
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

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route('/nanoid')
    def nanoid(n = 10):
        return jsonify({ "ndnoid": generate(size=n) })

def account(app):
        
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @app.route('/account_login',methods=["POST"])
    def login():
        try: 
            info = request.get_json()
            user_id = SQLHelper().fetch_one("select id from user where username = %s and password = %s", (info['username'], info['password']))
            if user_id:
                username = info['username']
                session[username] = user_id
                print(username, user_id)
                session.permanent = True
                token = TokenHelper().encrpyt_token(username)
            return jsonify({'code': 1, 'token': token})
        except:
            return jsonify({ 'code': 0, 'msg': '用户名或密码错误' })
    
    @app.route('/account_register',methods=['POST'])
    def register():
        try:
            info = request.get_json()
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            # newuser = SQLHelper().insert("insert into user(username, password, email, create_time, update_time) values (%s, %s, %s, %s, %s)", (
            #     info['username'], info['password'], info['email'], nowtime, nowtime
            # ))
            res = SQLHelper().insert('''
                insert into user(username, password, email, create_time, update_time) 
                select %s, %s, %s, %s, %s from DUAL where not exists 
                (select id from user where username = %s)''', (
                info['username'], info['password'], info['email'], nowtime, nowtime, info['username'],
            ))
            user_id = SQLHelper().execute("SELECT max(id) from user").get("max(id)")
            username = info['username']
            session[username] = user_id
            session.permanent = True
            token = TokenHelper().encrpyt_token(username)
            return {'code': 1, "token": token}
        except: 
            return jsonify({'code': 0, 'msg': "false"})

    # 登录
    @app.route('/account_get_userinfo', methods=['GET'])
    @is_login
    def get_userinfo(user_id):
        try: 
            user = SQLHelper().fetch_one('''select username, email, avatar from user where id = %s''', (user_id))
            return jsonify({ "code": 1, "userinfo": user })
        except: 
            return jsonify({ "code": 0, "msg": "失败" })

    @app.route('/account_upload_avatar', methods=['POST'])
    @is_login
    def upload_avatar(user_id):
        try:
            if 'avatar' not in request.files:
                return jsonify({"code": 0, "msg": "没有文件"})
            file = request.files['avatar']
            if file and allowed_file(file.filename):
                if file.filename == '':
                    return jsonify({"code": 0, "msg": "没有文件名"})
                # 原文件名
                filename = secure_filename(file.filename)
                # 新的随机文件名
                filename = "avatar_" + str(user_id) + '_' + generate(size=18) + '.' + filename.split(".")[-1]
                # 文件名存储
                SQLHelper().update('''update user set avatar =  %s where id = %s''', (filename, user_id))
                # 文件存储
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                return jsonify({"code": 1})
            return jsonify({"code": 0, "msg": "不允许上传"})
        except:
            return jsonify({"code": 0, "msg": "文件上传失败"})

    @app.route('/account_get_avatar', methods=['GET'])
    @is_login
    def get_avatar(user_id):
        try:
            user = SQLHelper().fetch_one('''select avatar from user where id = %s''', (user_id))
            avatar_url = url_for('static', filename = 'avatar/' + user.get('avatar'))
            return jsonify({'code': 1, 'avatar_url': avatar_url})
        except:
            return jsonify({'code': 0, "msg": "没有上传图片"})

    @app.route('/account_get_toberead', methods=['GET'])
    @is_login
    def get_toberead(user_id):
        try:
            toberead = SQLHelper().fetch_all('''
                SELECT a.id, a.title, a.url, a.nid 
                FROM (user_toberead d, article a) 
                WHERE (d.user_id = %s AND a.id = d.article_id)''', (user_id))
            return jsonify({"code": 1, "list": toberead})
        except:
            return jsonify({"code": 0, "msg": "获取待读失败"})

    @app.route('/account_get_history', methods=['GET'])
    @is_login
    def get_history(user_id):
        try:
            res = SQLHelper().fetch_all('''
                SELECT a.id, a.title, a.url, a.nid 
                FROM (user_history d, article a) 
                WHERE (d.user_id = %s AND a.id = d.article_id)''', (user_id))
            return jsonify({"code": 1, "list": res})
        except:
            return jsonify({"code": 0, "msg": "获取足迹失败"})

    @app.route('/account_get_favorite', methods=['GET'])
    @is_login
    def get_favorite(user_id):
        try:
            res = SQLHelper().fetch_all('''
                SELECT a.id, a.title, a.url, a.nid 
                FROM (user_favorite d, article a) 
                WHERE (d.user_id = %s AND a.id = d.article_id)''', (user_id))
            return jsonify({"code": 1, "list": res})
        except:
            return jsonify({"code": 0, "msg": "获取收藏失败"})

    @app.route('/account_get_excerpt',methods=["GET"])
    @is_login
    def get_excerpt(user_id):
        try: 
            res = SQLHelper().fetch_all('''
                SELECT *
                FROM user_excerpt 
                WHERE user_id = %s''', (user_id))
            return jsonify({'code': 1, 'list': res})
        except:
            return jsonify({ 'code': 0, 'msg': '获取评论失败' })

def article(app):

    @app.route('/get_article',methods=["GET"])
    @is_login
    def get_article(user_id):
        try: 
            article_id = request.args["article_id"]
            res = SQLHelper().fetch_all('''
                SELECT *
                FROM article
                WHERE id = %s''', (
                    article_id
                ))
            return jsonify({'code': 1, 'list': res})
        except:
            return jsonify({ 'code': 0, 'msg': '获取评论失败' })



    @app.route('/article_toberead',methods=["GET"])
    @is_login
    def toberead(user_id):
        try: 
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            article_id = request.args.get("article_id")
            res = SQLHelper().insert('''
                insert into user_toberead(user_id, article_id, create_time) 
                select %s, %s, %s from DUAL where not exists 
                (select id from user_toberead where user_id = %s and article_id = %s)''', (
                user_id, article_id, nowtime, user_id, article_id))
            return jsonify({'code': 1})
        except:
            return jsonify({ 'code': 0, 'msg': '加入待读失败' })

    @app.route('/article_history',methods=["GET"])
    @is_login
    def history(user_id):
        try: 
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            article_id = request.args.get("article_id")
            res = SQLHelper().insert('''
                insert into user_history(user_id, article_id, create_time) 
                select %s, %s, %s from DUAL where not exists 
                (select id from user_history where user_id = %s and article_id = %s)''', (
                user_id, article_id, nowtime, user_id, article_id))
            return jsonify({'code': 1})
        except:
            return jsonify({ 'code': 0, 'msg': '加入足迹失败' })

    @app.route('/article_favorite',methods=["GET"])
    @is_login
    def favorite(user_id):
        try: 
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            article_id = request.args.get("article_id")
            res = SQLHelper().insert('''
                insert into user_favorite(user_id, article_id, create_time) 
                select %s, %s, %s from DUAL where not exists 
                (select id from user_favorite where user_id = %s and article_id = %s)''', (
                user_id, article_id, nowtime, user_id, article_id))
            return jsonify({'code': 1})
        except:
            return jsonify({ 'code': 0, 'msg': '加入收藏失败' })

    @app.route('/article_comment',methods=["POST"])
    @is_login
    def comment(user_id):
        try: 
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            article_id = request.get_json()["article_id"]
            comment = request.get_json()["comment"]
            res = SQLHelper().insert('''
                INSERT INTO comment_article(user_id, comment, article_id, create_time) 
                VALUES (%s, %s, %s, %s)''', (
                user_id, comment, article_id, nowtime))
            return jsonify({'code': 1})
        except:
            return jsonify({ 'code': 0, 'msg': '评论失败' })

    @app.route('/article_get_comment',methods=["GET"])
    @is_login
    def get_comment(user_id):
        try: 
            article_id = request.args["article_id"]
            res = SQLHelper().fetch_all('''
                SELECT c.user_id, u.username, c.comment, c.create_time
                FROM (comment_article c, user u)
                WHERE (c.article_id = %s AND u.id = c.user_id)
                LIMIT 3 OFFSET 0''', (
                    article_id
                ))
            return jsonify({'code': 1, 'list': res})
        except:
            return jsonify({ 'code': 0, 'msg': '获取评论失败' })

    @app.route('/article_get_article',methods=["GET"])
    @is_login
    def article_get_article(user_id):
        try: 
            article_id = request.args["article_id"]
            res = SQLHelper().fetch_all('''
                SELECT *
                FROM article
                WHERE id = %s''', (
                    article_id
                ))
            return jsonify({'code': 1, 'list': res})
        except:
            return jsonify({ 'code': 0, 'msg': '获取评论失败' })

def sentence(app):
    @app.route('/sentence_comment',methods=["POST"])
    @is_login
    def comment2(user_id):
        try: 
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            article_id = request.get_json()["article_id"]
            sentence = request.get_json()["sentence"]
            comment = request.get_json()["comment"]
            father_id = request.get_json().get('comment_id', 0)
            SQLHelper().insert('''
                INSERT INTO sentence(sentence, article_id)
                VALUES (%s, %s)''', (
                sentence, article_id))
            # sentence_id = SQLHelper().execute("SELECT LAST_INSERT_ID()").get('LAST_INSERT_ID()')
            # print(sentence_id)
            sentence_id = SQLHelper().execute("SELECT max(id) from sentence").get("max(id)")
            res = SQLHelper().insert('''
                INSERT INTO comment_sentence(user_id, comment, sentence_id, father_id, create_time) 
                VALUES (%s, %s, %s, %s, %s)''', (
                user_id, comment, sentence_id, father_id, nowtime))
            return jsonify({'code': 1})
        except:
            return jsonify({ 'code': 0, 'msg': '评论失败' })

    @app.route('/sentence_get_comment',methods=["GET"])
    @is_login
    def get_sentencecomment2(user_id):
        try: 
            sentence_id = request.args["sentence_id"]
            res = SQLHelper().fetch_all('''
                SELECT c.id, c.user_id, u.username, c.comment, c.father_id, c.create_time
                FROM (comment_sentence c, user u)
                WHERE (c.sentence_id = %s AND u.id = c.user_id)
                ''', (
                    sentence_id
                ))
            return jsonify({'code': 1, 'list': res})
        except:
            return jsonify({ 'code': 0, 'msg': '获取评论失败' })

    @app.route('/sentence_excerpt',methods=["POST"])
    @is_login
    def excerpt(user_id):
        try: 
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            article_id = request.get_json()["article_id"]
            sentence = request.get_json()["sentence"]
            comment = request.get_json()["comment"]
            SQLHelper().insert('''
                INSERT INTO user_excerpt(user_id, sentence, article_id, comment, create_time)
                VALUES (%s, %s, %s, %s, %s)''', (
                user_id, sentence, article_id, comment, create_time))
            return jsonify({'code': 1})
        except:
            return jsonify({ 'code': 0, 'msg': '新建摘记失败' })

def megazine(app):
    @app.route('/megazine_get_summarys',methods=["GET"])
    def get_summarys():
        try: 
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            category = request.args.get("category")
            res = SQLHelper.fetch_all('''
                SELECT id, title, author, summary, link, content
                FROM article
                WHERE category = %s
                ORDER BY RAND() LIMIT 20''', (category))
            return {'code': 1, 'list': res}
        except:
            return { 'code': 0, 'msg': '获取杂志失败' }






def configure_cross(app):
    @app.after_request
    def cors(environ):
        environ.headers['Access-Control-Allow-Origin']='*'
        environ.headers['Access-Control-Allow-Method']='*'
        environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
        return environ

app = create_app()
app.run(debug=IS_SERVERLESS != True, port=9000, host='0.0.0.0')
