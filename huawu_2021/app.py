 
import sys
sys.path.append(".")
import os
import time
import json
from os import path
from datetime import timedelta

from nanoid import generate
import pymysql
from flask import jsonify, Flask, flash, request, redirect, current_app, session, url_for, send_from_directory
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
            host='xxx',
            port=000,
            user='xxx',
            password='xxx',
            database='demo',#链接的数据库的名字
            charset='utf8'
        ),
        # 配置原生文件上传, 覆盖
        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}, # 允许上传的文件类型
        MAX_CONTENT_LENGTH = 16 * 1000 * 1000,  # 最大文件大小 16M
    )
    configure_folders(app)
    configure_handler(app)
    configure_cross(app)
    account(app)
    article(app)
    sentence(app)
    megazine(app)
    tags(app)
    return app

def configure_folders(app):
    # 初始化上传临时目录
    UPLOAD_DIR = '/tmp/uploads' if IS_SERVERLESS else os.getcwd() + '/uploads'
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    app.config['UPLOAD_DIR'] = UPLOAD_DIR

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

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_DIR'], filename)

def account(app):

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @app.route('/account_login',methods=["POST"])
    def account_login():
        try:
            info = request.get_json()
            user = SQLHelper().fetch_one("select id, tags from user where username = %s and password = %s", (info['username'], info['password']))
            if user:
                username = info['username']
                token = TokenHelper().encrpyt_token(user['id'])
                if user['tags'] != None:
                    flag = True
                else:
                    flag = False
            return jsonify({'code': 1, 'token': token, 'flag': flag})
        except:
            return jsonify({ 'code': 0, 'msg': '用户名或密码错误' })

    @app.route('/account_register',methods=['POST'])
    def account_register():
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
            return jsonify({'code': 1, "token": token})
        except:
            return jsonify({'code': 0, 'msg': "false"})

    @app.route('/account_get_selfinfo', methods=['GET'])
    @is_login
    def account_get_selfinfo(user_id):
        try:
            user = SQLHelper().fetch_one('''select username, email, avatar, create_time from user where id = %s''', (user_id))
            filename = user.get('avatar')
            if filename == None:
                avatar_url = None
            else:
                avatar_url = "/test/uploads/" + filename
            user['avatar'] = avatar_url
            return jsonify({ "code": 1, "userinfo": user })
        except:
            return jsonify({ "code": 0, "msg": "失败" })

    @app.route('/account_get_userinfo', methods=['GET'])
    def account_get_userinfo():
        try:
            user_id = request.args["user_id"]
            try:
                user = SQLHelper().fetch_one('''select username, email, avatar, create_time from user where id = %s''', (user_id))
                filename = user.get('avatar')
            except:
                return jsonify({"code": "0", "msg": "查询失败"})
            avatar_url = "/test/uploads/" + filename
            user['avatar'] = avatar_url
            return jsonify({ "code": 1, "userinfo": user })
        except:
            return jsonify({ "code": 0, "msg": "失败" })

    @app.route('/account_upload_avatar', methods=['POST'])
    @is_login
    def account_upload_avatar(user_id):
        try:
            if 'avatar' not in request.files:
                return jsonify({"code": 0, "msg": "没有文件"})
            file = request.files['avatar']
            if allowed_file(file.filename):
                if file.filename == '':
                    return jsonify({"code": 0, "msg": "没有文件名"})
                try: # 原文件名 # 新的随机文件名
                    filename = secure_filename(file.filename)
                    filename = "avatar_" + str(user_id) + '_' + generate(size=18) + '.' + filename.split(".")[-1]
                    filePath = os.path.join(app.config['UPLOAD_DIR'], filename)
                except:
                    return jsonify({"code": 0, "msg": "获取文件名失败"})
                try: # 文件名存储
                    SQLHelper().update('''update user set avatar =  %s where id = %s''', (filename, user_id))
                except:
                    return jsonify({"code": 0, "msg": "数据库保存失败"})
                try: # 文件存储
                    file.save(filePath)
                    # file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                except:
                    return jsonify({"code": 0, "msg": "文件保存失败", "filename": filename})

                try:
                    uploadUrl = "/test/uploads/" + filename
                    return jsonify({"code": 1, "url": uploadUrl})
                except:
                    return jsonify({"code": 0, "msg": "莫名其妙"})
            return jsonify({"code": 0, "msg": "不允许上传该类型", "isAllowed": allowed_file(file.filename)})
        except:
            return jsonify({"code": 0, "msg": "文件上传失败"})

    @app.route('/account_get_avatar', methods=['GET'])
    @is_login
    def account_get_avatar(user_id):
        try:
            user = SQLHelper().fetch_one('''select avatar from user where id = %s''', (user_id))
            filename = user.get('avatar')
            avatar_url = "/test/uploads/" + filename
            return jsonify({'code': 1, 'avatar_url': avatar_url})
        except:
            return jsonify({'code': 0, "msg": "没有上传图片"})

    @app.route('/account_get_toberead', methods=['GET'])
    @is_login
    def account_get_toberead(user_id):
        try:
            toberead = SQLHelper().fetch_all('''
                SELECT d.id as record_id, a.id, a.title, a.link
                FROM (user_toberead d, article a)
                WHERE d.user_id = %s AND d.article_id = a.id''', (user_id))
            return jsonify({"code": 1, "list": toberead})
        except:
            return jsonify({"code": 0, "msg": "获取待读失败"})

    @app.route('/account_get_history', methods=['GET'])
    @is_login
    def account_get_history(user_id):
        try:
            res = SQLHelper().fetch_all('''
                SELECT d.id as record_id, a.id, a.title, a.link
                FROM (user_history d, article a)
                WHERE (d.user_id = %s AND a.id = d.article_id)''', (user_id))
            return jsonify({"code": 1, "list": res})
        except:
            return jsonify({"code": 0, "msg": "获取足迹失败"})

    @app.route('/account_get_favorite', methods=['GET'])
    @is_login
    def account_get_favorite(user_id):
        try:
            res = SQLHelper().fetch_all('''
                SELECT d.id as record_id, a.id, a.title, a.link
                FROM (user_favorite d, article a)
                WHERE (d.user_id = %s AND a.id = d.article_id)''', (user_id))
            return jsonify({"code": 1, "list": res})
        except:
            return jsonify({"code": 0, "msg": "获取收藏失败"})

    @app.route('/account_get_excerpt',methods=["GET"])
    @is_login
    def account_get_excerpt(user_id):
        try:
            res = SQLHelper().fetch_all('''
                SELECT *
                FROM user_excerpt
                WHERE user_id = %s''', (user_id))
            return jsonify({'code': 1, 'list': res})
        except:
            return jsonify({ 'code': 0, 'msg': '获取摘记失败' })

    @app.route('/account_delete', methods=["GET"])
    def account_delete():
        try:
            record_id = request.args["record_id"]
            tableid = request.args["table_id"]
            if tableid == 1 or tableid=="1":
                SQLHelper.delete("delete from user_favorite where id = %s", (int(record_id)))
            elif tableid == 2 or tableid=="2":
                SQLHelper.delete("delete from user_toberead where id = %s", (int(record_id)))
            elif tableid == 3 or tableid=="3":
                SQLHelper.delete("delete from user_history where id = %s", (int(record_id)))
            elif tableid == 4 or tableid=="4":
                SQLHelper.delete("delete from user_excerpt where id = %s", (int(record_id)))
            else:
                return jsonify({"code": 0, "msg": "没有该tableid"})
            return jsonify({"code": 1, "msg": "删除成功"})
        except:
            return jsonify({"code": 0, "msg": "删除记录失败"})

def tags(app):
    @app.route('/tag_get_tags', methods=['GET'])
    def tag_get_tags():
        try:
            res = ["创业", "第九区", "技术", "科技", "区块链", "设计", "数码"]

            return jsonify({"code": 1, "list": res})
        except:
            return jsonify({"code": 0, "msg": "获取标签失败"})

    @app.route('/tag_set_tags', methods=['POST'])
    @is_login
    def tag_set_tags(user_id):
        try:
            args = request.get_json()['args']
            args = str(args)
            SQLHelper.update('''
                update user set tags = %s where id = %s
            ''', (args, user_id))
            res = SQLHelper.fetch_one("SELECT * from user where id = %s", user_id)
            args = res['tags']
            args = list(eval(args))
            return jsonify({"code": 1, "res": args})
        except:
            return jsonify({"code": 0, "msg": "设置标签失败"})

    @app.route('/reduce_5percent', methods=['GET'])
    def reduce_5percent():
        try:
            def user_dictionary_decrease(dictionary):
                dictionary = json.loads(dictionary)
                for key, value in dictionary.items():
                    value *= 0.9
                    dictionary[key] = value
            sql = "select id, dictionary from user where dictionary is not null"
            results = SQLHelper.fetch_all(sql, ())
            for result in results:
                user_dictionary_decrease(result[1])
            return jsonify({"code": 1, "msg": "更新历史成功"})
        except:
            return jsonify({"code": 0, "msg": "更新历史失败"})

def article(app):

    @app.route('/article_toberead',methods=["GET"])
    @is_login
    def article_toberead(user_id):
        try:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            article_id = request.args.get("article_id")
            res = SQLHelper().insert('''
                insert into user_toberead(user_id, article_id, create_time)
                select %s, %s, %s from DUAL where not exists
                (select id from user_toberead where user_id = %s and article_id = %s)''', (
                user_id, article_id, nowtime, user_id, article_id))
            max_id = SQLHelper().execute("SELECT max(id) from user_toberead").get("max(id)")

            return jsonify({'code': 1, 'id': max_id})
        except:
            return jsonify({ 'code': 0, 'msg': '加入待读失败' })

    @app.route('/article_history',methods=["GET"])
    @is_login
    def article_history(user_id):
        try:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            article_id = request.args.get("article_id")
            # 判断是否已经加入到历史记录里面过
            res = SQLHelper.fetch_one('''
                select id
                from user_history
                where user_id = %s and article_id = %s''', (user_id, article_id))
            # 如果已经加入过，就更新插入日期
            if res:
                history_id = res['id']
                res = SQLHelper().update('''UPDATE user_history SET update_time = %s WHERE id = %s''', (nowtime, history_id))
                return jsonify({'code': 1, "msg": "不是新的记录"})
            # 如果是新的浏览记录，就插入新的，同时更新用户的浏览记录列表供个性化推荐使用
            else:
                try:
                    # 插入一条浏览记录
                    res = SQLHelper().insert('''
                        INSERT INTO user_history(user_id, article_id, create_time, update_time)
                        VALUES (%s, %s, %s, %s)''', (user_id, article_id, nowtime, nowtime))
                    # 更新user下的history
                    res = SQLHelper.fetch_all('''
                        SELECT article_id from user_history
                        WHERE user_id = %s''', (user_id))
                    histories = [json['article_id'] for json in res]
                    article_ids_str = ",".join(map(str, histories))
                    SQLHelper().update('''UPDATE user SET history = %s WHERE id = %s''', (article_ids_str, user_id))
                except:
                    return jsonify({"code": 0, "msg": "更新history失败"})
                try:
                    # 更新user下的dictionary
                    try:

                        user = SQLHelper.fetch_one('''
                            SELECT dictionary from user
                            WHERE id = %s''', (user_id))
                        if (user['dictionary'] == None):
                            dictionary = {}
                        else:
                            dictionary = json.loads(user['dictionary'])
                    except:
                        return jsonify({"code": 0, "msg": "读取用户爱好字典失败"})
                    for history in histories:
                        try:
                            dic_result = SQLHelper.fetch_one("select keywords from article where id = %s", (history))
                            if dic_result == None:
                                continue
                            try:
                                dic_result = json.loads(dic_result['keywords'])
                            except:
                                return jsonify({"code": 0, "msg": dic_result})
                                continue
                        except:
                            return jsonify({"code": 0, "msg": "该文章没有keyword列表"})
                        for key, value in dic_result.items():
                            if key in dictionary.keys():
                                dictionary[key] += value
                            else:
                                dictionary[key] = value
                    SQLHelper.update(
                        "update user set dictionary = %s where id = %s",
                        (json.dumps(dictionary, ensure_ascii = False), user_id))
                except:
                    return jsonify({"code": 0, "msg": "更新字典失败"})
            return jsonify({'code': 1})
        except:
            return jsonify({ 'code': 0, 'msg': '加入足迹失败' })

    @app.route('/article_favorite',methods=["GET"])
    @is_login
    def article_favorite(user_id):
        try:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            article_id = request.args.get("article_id")
            res = SQLHelper().insert('''
                insert into user_favorite(user_id, article_id, create_time)
                select %s, %s, %s from DUAL where not exists
                (select id from user_favorite where user_id = %s and article_id = %s)''', (
                user_id, article_id, nowtime, user_id, article_id))
            max_id = SQLHelper().execute("SELECT max(id) from user_favorite").get("max(id)")

            return jsonify({'code': 1, "id": max_id})
        except:
            return jsonify({ 'code': 0, 'msg': '加入收藏失败' })

    # 评论文章
    @app.route('/article_comment',methods=["POST"])
    @is_login
    def article_comment(user_id):
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
    def article_get_comment():
        try:
            article_id = request.args["article_id"]
            res = SQLHelper().fetch_all('''
                SELECT c.id as record_id, c.user_id, u.username, c.comment, c.create_time
                FROM (comment_article c, user u)
                WHERE (c.article_id = %s AND u.id = c.user_id)
                ''', (
                    article_id
                ))
            return jsonify({'code': 1, 'list': res})
        except:
            return jsonify({ 'code': 0, 'msg': '获取评论失败' })

    @app.route('/article_get_article',methods=["GET"])
    def article_get_article():
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

    @app.route('/article_get_sentence_comment',methods=["GET"])
    def article_get_sentence_comment():
        try:
            article_id = request.args["article_id"]
            res = SQLHelper().fetch_all('''
                SELECT s.id as sentence_id, s.sentence, cs.id as record_id, cs.user_id, cs.comment, cs.create_time, u.username
                FROM sentence s, comment_sentence cs, user u
                WHERE s.article_id = %s AND cs.sentence_id = s.id AND u.id = cs.user_id''', (
                    article_id
                ))
            b = []
            a = {}
            for itemm in list(res):
                if itemm["sentence_id"] in a.keys():
                    a[itemm["sentence_id"]].append(itemm)
                else:
                    a[itemm["sentence_id"]] = [itemm]
                pass
            for k, v in a.items():
                b.append({
                    "sentence_id": k,
                    "list": v
                })

            return jsonify({'code': 1, 'list': b})
        except:
            return jsonify({ 'code': 0, 'msg': '获取画线评论失败' })

    @app.route('/article_insert_article',methods=["POST"])
    def article_insert_article():
        try:
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            title = request.get_json()["title"]
            summary = request.get_json().get("summary", None)
            content = request.get_json()["content"]
            author = request.get_json()["author"]
            link = request.get_json()["link"]
            category = request.get_json()["category"]
            res = SQLHelper().insert('''
                INSERT INTO article(title, summary, content, author, link, create_time, category)
                VALUES (%s, %s, %s, %s, %s, %s, %s)''', (
                title, summary, content, author, link, create_time, category))
            return jsonify({'code': 1})
        except:
            return jsonify({ 'code': 0, 'msg': '获取评论失败' })

def sentence(app):

    @app.route('/sentence_get_some_sentence',methods=["GET"])
    def sentence_get_some_sentence():
        try:
            res = SQLHelper.fetch_all('''
                SELECT *
                FROM user_excerpt
                ORDER BY RAND() LIMIT 20''', ())
            res = [{"sentence": exc['sentence'], "article_id" :exc["article_id"]} for exc in res if len(exc["sentence"]) < 25]
            return jsonify({'code': 1, 'list': res})
        except:
            return jsonify({ 'code': 0, 'msg': '获取划线句子失败' })

    # @app.route('/sentence_get_some_sentence',methods=["GET"])
    # def sentence_get_some_sentence():
    #     try:
    #         res = SQLHelper.fetch_all('''
    #             SELECT *
    #             FROM sentence
    #             ORDER BY RAND() LIMIT 5''', ())
    #         return jsonify({'code': 1, 'list': res})
    #     except:
    #         return jsonify({ 'code': 0, 'msg': '获取划线句子失败' })


    # 画线评论
    @app.route('/sentence_comment',methods=["POST"])
    @is_login
    def sentence_comment(user_id):
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

    # 评论被画线的句子
    @app.route('/sentence_comment2',methods=["POST"])
    @is_login
    def sentence_comment2(user_id):
        try:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sentence_id = request.get_json()["sentence_id"]
            comment = request.get_json()["comment"]
            father_id = request.get_json().get('father_id', 0)
            res = SQLHelper().insert('''
                INSERT INTO comment_sentence(user_id, comment, sentence_id, father_id, create_time)
                VALUES (%s, %s, %s, %s, %s)''', (
                user_id, comment, sentence_id, father_id, nowtime))
            return jsonify({'code': 1})
        except:
            return jsonify({ 'code': 0, 'msg': '评论失败' })

    @app.route('/sentence_get_comment',methods=["GET"])
    def sentence_get_comment():
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
    def sentence_excerpt(user_id):
        try:
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            article_id = request.get_json()["article_id"]
            sentence = request.get_json()["sentence"]
            comment = request.get_json()["comment"]
            SQLHelper().insert('''
                INSERT INTO user_excerpt(user_id, sentence, article_id, comment, create_time)
                VALUES (%s, %s, %s, %s, %s)''', (
                user_id, sentence, article_id, comment, create_time))
            max_id = SQLHelper().execute("SELECT max(id) from user_excerpt").get("max(id)")

            return jsonify({'code': 1, 'id': max_id})
        except:
            return jsonify({ 'code': 0, 'msg': '新建摘记失败' })

def megazine(app):

    @app.route('/megazine_get_randomly',methods=["GET"])
    def megazine_get_randomly():
        try:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            res = SQLHelper.fetch_all('''
                SELECT id, title, author, summary
                FROM article
                ORDER BY RAND() LIMIT 20''', ())
            res2 = [ article['id'] for article in res]

            return jsonify({'code': 1, 'list': res2, 'list2': res})
        except:
            return jsonify({ 'code': 0, 'msg': '获取杂志(文章列表)失败' })


    @app.route('/megazine_get_summarys',methods=["GET"])
    def megazine_get_summarys():
        try:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            category = request.args.get("category")
            res = SQLHelper.fetch_all('''
                SELECT id, title, author, summary, link, content
                FROM article
                WHERE category = %s
                ORDER BY RAND() LIMIT 20''', (category))
            return jsonify({'code': 1, 'list': res})
        except:
            return jsonify({ 'code': 0, 'msg': '获取杂志(文章列表)失败' })

    @app.route('/megazine_get_megazine',methods=["GET"])
    def megazine_get_megazines():
        try:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            category = request.args.get("category")
            res = SQLHelper.fetch_all('''
                SELECT id
                FROM article
                WHERE category = %s
                ORDER BY RAND() LIMIT 20''', (category))
            res = [ article['id'] for article in res]
            return jsonify({'code': 1, 'title': '一个杂志的标题', 'cover': None, 'list': res})
        except:
            return jsonify({ 'code': 0, 'msg': '获取杂志(文章列表)失败' })

    @app.route('/megazine_get_recommends',methods=["GET"])
    @is_login
    def megazine_get_recommends(user_id):
        try:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            try:
                # 查询用户的关键词
                user = SQLHelper.fetch_one('''
                    SELECT *
                    FROM user
                    WHERE id = %s''', (user_id))
            except:
                return jsonify({"code": 0, "msg": "查询文章失败"})
            dictionary = user['dictionary']
            history = user['history']
            first_open = user['first_read']
            tags = user['tags']
            if dictionary:
                dictionary = json.loads(dictionary)
            else:
                dictionary = {}
            # 随机查询文章
            results = SQLHelper.fetch_all('''
                SELECT id, keywords
                FROM article
                ORDER BY RAND() LIMIT 20''', ())
            if dictionary == {} or dictionary == None:
                if tags == None or tags == "":
                    recommend = [ resu['id'] for resu in results]
                    msg = "冷启动"
                else:
                    tags = list(eval(tags))
                    recommend = []
                    for tag in tags:
                        ready_articles = SQLHelper.fetch_all('''
                            SELECT id
                            FROM article WHERE category = %s
                            ORDER BY RAND() LIMIT 5''', (tag))
                        recommend += ready_articles
                    recommend = [rec['id'] for rec in recommend]
                    msg = "根据标签推荐"
            else:
                if first_open == 0:
                    SQLHelper.update('''
                        update user set first_read = 1 where id = %s
                    ''', (user_id))
                # 计算相关性并排序
                topK = []
                rel = ()
                try:
                    for result in results:
                        keywords = json.loads(result["keywords"])
                        article_sum = 0
                        for key, value in keywords.items():
                            if key in dictionary.keys():
                                article_sum += value * dictionary[key]
                        rel = (article_sum, result['id'])
                        topK.append(rel)
                except:
                    return jsonify({"code": 1, "msg": "加载文章键字失败"})
                topK.sort(reverse = True) # 从大到小排序, article_sum为文章与用户字典的相关度, result[0]为推荐的文章id, result[2]为推荐的文章内容
                recommend = []
                for index in range(10):
                    recommend.append(topK[index][1])
                msg = "正常推荐"
            return jsonify({'code': 1, 'list': recommend, "msg": msg})
        except:
            return jsonify({ 'code': 0, 'msg': '获取个性化推荐列表失败' })

def configure_cross(app):
    @app.after_request
    def cors(environ):
        environ.headers['Access-Control-Allow-Origin']='*'
        environ.headers['Access-Control-Allow-Method']='*'
        environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
        return environ

app = create_app()
app.run(debug=IS_SERVERLESS != True, port=9000, host='0.0.0.0')
