import os
import sys
import time

from flask import Blueprint, render_template, request, session, redirect, current_app, flash, url_for

sys.path.append(".")
from utils.db import SQLHelper
from utils.wrappers import *

megazine = Blueprint('megazine', __name__, url_prefix='/megazine')

@megazine.route('/get_summarys',methods=["GET"])
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
        return { 'code': 0, 'msg': '加入待读失败' }























