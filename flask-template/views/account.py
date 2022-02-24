import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

import time

from nanoid import generate
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, session, redirect, current_app, flash, url_for

from utils.db import SQLHelper
from utils.tokenUtil import TokenHelper
from utils.wrappers import *

account = Blueprint('account', __name__, url_prefix='/account')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
def allowed_file(filename):
    print(filename.rsplit('.', 1))
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# 未登录
@account.route('/login',methods=["POST"])
def login():
    try: 
        info = request.get_json()
        user_id = SQLHelper().fetch_one("select id from user where username = %s and password = %s", (info['username'], info['password']))
        print(user_id)
        print(user_id['id'])
        if user_id:
            username = info['username']
            session[username] = user_id
            print(username, user_id)
            session.permanent = True
            token = TokenHelper().encrpyt_token(username)
        return {'code': 1, 'token': token}
    except:
        return { 'code': 0, 'msg': '用户名或密码错误' }

@account.route('/register',methods=['POST'])
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
        return {'code': 0, 'msg': "false"}

# 登录
@account.route('/get_userinfo', methods=['GET'])
@is_login
def get_userinfo(user_id):
    try: 
        user = SQLHelper().fetch_one('''select username, email, avatar from user where id = %s''', (user_id))
        return { "code": 1, "userinfo": user }
    except: 
        return { "code": 0, "msg": "失败" }

@account.route('/upload_avatar', methods=['POST'])
@is_login
def upload_avatar(user_id):
    try:
        if 'avatar' not in request.files:
            return jsonify({"code": 0, "msg": "没有文件"})
        file = request.files['avatar']
        if allowed_file(file.filename):
            if file.filename == '':
                return jsonify({"code": 0, "msg": "没有文件名"})
            # 原文件名
            filename = secure_filename(file.filename)
            # 新的随机文件名
            filename = "avatar_" + str(user_id) + '_' + generate(size=18) + '.' + filename.split(".")[-1]
            try:
                # 文件名存储
                SQLHelper().update('''update user set avatar =  %s where id = %s''', (filename, user_id))
            except:
                return jsonify({"code": 0, "msg": "数据库保存错误"})
            # 文件存储
            try:
                # file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                file.save(os.path.join(filename))
                return jsonify({"code": 1})
            except:
                return jsonify({"code": 0, "msg": "文件保存错误"})
        return jsonify({"code": 0, "msg": "不允许上传该类型", "isAllowed": allowed_file(file.filename)})
    except:
        return jsonify({"code": 0, "msg": "文件上传失败"})
    # try:
    #     if 'avatar' not in request.files:
    #         return {"code": 0, "msg": "没有文件"}
    #     file = request.files['avatar']
    #     if file and allowed_file(file.filename):
    #         if file.filename == '':
    #             return {"code": 0, "msg": "没有文件名"}
    #         # 原文件名
    #         filename = secure_filename(file.filename)
    #         # 新的随机文件名
    #         filename = "avatar_" + str(user_id) + '_' + generate(size=18) + '.' + filename.split(".")[-1]
    #         # 文件名存储
    #         SQLHelper().update('''update user set avatar =  %s where id = %s''', (filename, user_id))
    #         # 文件存储
    #         file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    #         return {"code": 1}
    #     return {"code": 0, "msg": "不允许上传"}
    # except:
    #     return {"code": 0, "msg": "文件上传失败"}

@account.route('/get_avatar', methods=['GET'])
@is_login
def get_avatar(user_id):
    try:
        user = SQLHelper().fetch_one('''select avatar from user where id = %s''', (user_id))
        avatar_url = url_for('static', filename = 'avatar/' + user.get('avatar'))
        return {'code': 1, 'avatar_url': avatar_url}
    except:
        return {'code': 0, "msg": "没有上传图片"}

@account.route('/get_toberead', methods=['GET'])
@is_login
def get_toberead(user_id):
    try:
        toberead = SQLHelper().fetch_all('''
            SELECT a.id, a.title, a.url, a.nid 
            FROM (user_toberead d, article a) 
            WHERE (d.user_id = %s AND a.id = d.article_id)''', (user_id))
        return {"code": 1, "list": toberead}
    except:
        return {"code": 0, "msg": "获取待读失败"}

@account.route('/get_history', methods=['GET'])
@is_login
def get_history(user_id):
    try:
        res = SQLHelper().fetch_all('''
            SELECT a.id, a.title, a.url, a.nid 
            FROM (user_history d, article a) 
            WHERE (d.user_id = %s AND a.id = d.article_id)''', (user_id))
        return {"code": 1, "list": res}
    except:
        return {"code": 0, "msg": "获取足迹失败"}

@account.route('/get_favorite', methods=['GET'])
@is_login
def get_favorite(user_id):
    try:
        res = SQLHelper().fetch_all('''
            SELECT a.id, a.title, a.url, a.nid 
            FROM (user_favorite d, article a) 
            WHERE (d.user_id = %s AND a.id = d.article_id)''', (user_id))
        return {"code": 1, "list": res}
    except:
        return {"code": 0, "msg": "获取收藏失败"}

@account.route('/get_excerpt',methods=["GET"])
@is_login
def get_excerpt(user_id):
    try: 
        res = SQLHelper().fetch_all('''
            SELECT *
            FROM user_excerpt 
            WHERE user_id = %s''', (user_id))
        return {'code': 1, 'list': res}
    except:
        return { 'code': 0, 'msg': '获取评论失败' }



