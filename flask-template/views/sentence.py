import os
import sys
import time

from flask import Blueprint, render_template, request, session, redirect, current_app, flash, url_for

sys.path.append(".")
from utils.db import SQLHelper
from utils.wrappers import *

sentence = Blueprint('sentence', __name__, url_prefix='/sentence')


@sentence.route('/comment',methods=["POST"])
@is_login
def comment(user_id):
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
        return {'code': 1}
    except:
        return { 'code': 0, 'msg': '评论失败' }

@sentence.route('/comment2',methods=["POST"])
@is_login
def comment2(user_id):
    try: 
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        sentence_id = request.get_json()["sentence_id"]
        comment = request.get_json()["comment"]
        father_id = request.get_json().get('father_id', 0)
        res = SQLHelper().insert('''
            INSERT INTO comment_sentence(user_id, comment, sentence_id, father_id, create_time) 
            VALUES (%s, %s, %s, %s, %s)''', (
            user_id, comment, sentence_id, father_id, nowtime))
        return {'code': 1}
    except:
        return { 'code': 0, 'msg': '评论失败' }


@sentence.route('/get_comment',methods=["GET"])
def get_comment():
    try: 
        sentence_id = request.args["sentence_id"]
        res = SQLHelper().fetch_all('''
            SELECT c.id, c.user_id, u.username, c.comment, c.father_id, c.create_time
            FROM (comment_sentence c, user u)
            WHERE (c.sentence_id = %s AND u.id = c.user_id)
            LIMIT 3 OFFSET 0''', (
                sentence_id
            ))
        return {'code': 1, 'list': res}
    except:
        return { 'code': 0, 'msg': '获取评论失败' }

@sentence.route('/excerpt',methods=["POST"])
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
        return {'code': 1}
    except:
        return { 'code': 0, 'msg': '新建摘记失败' }

@sentence.route('/get_some_sentence',methods=["GET"])
def get_some_sentence():
    try: 
        res = SQLHelper.fetch_all('''
            SELECT id, sentence, article_id
            FROM sentence
            ORDER BY RAND() LIMIT 5''', ())
        return {'code': 1, 'list': res}
    except:
        return { 'code': 0, 'msg': '获取划线句子失败' }

@sentence.route('/get_some_sentence_and_comment',methods=["GET"])
def get_some_sentence_and_comment():
    try: 
        res = SQLHelper.fetch_all('''
            SELECT sentence, article_id
            FROM sentence
            ORDER BY RAND() LIMIT 5''', ())
        return {'code': 1, 'list': res}
    except:
        return { 'code': 0, 'msg': '获取划线句子失败' }










