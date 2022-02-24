import sys
sys.path.append(".")

from functools import wraps

from flask import request, redirect, current_app, session, jsonify

from utils.tokenUtil import TokenHelper

# 登录拦截器
def is_login(func):
    @wraps(func)
    def wrapper():
        if request.path == "/account/login":
            return None
        else:
            try:
                token = request.headers["Authorization"]
                header_info = TokenHelper.decrypt_token(token)
                username = header_info.get("username")
                user = session.get(username)
                user_id = user.get("id")
                return func(user_id)
            except:
                return jsonify({'msg': 'token 验证失败'})
    wrapper.__name__ = func.__name__
    return wrapper