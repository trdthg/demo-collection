 
import sys,os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')

from functools import wraps

from flask import jsonify, request, redirect, current_app, session

from utils.tokenUtil import TokenHelper

# 登录拦截器
def is_login(func):
    @wraps(func)
    def wrapper():
        try:
            token = request.headers["Authorization"]
            print(request.headers)
            try:
                header_info = TokenHelper.decrypt_token(token)
                user_id = header_info.get("user_id")
                try:
                    return func(user_id)
                except:
                    return jsonify({"code": -1, "msg": "验证成功, 函数内部执行失败, 请call我来修"})
            except:
                    return jsonify({'code': 0, 'msg': 'token 解码失败'})
        except:
            return jsonify({'code': 0, 'msg': '没有得到Authorization'})
    wrapper.__name__ = func.__name__
    return wrapper
