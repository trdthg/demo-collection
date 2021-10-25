#coding: utf-8
import time
import json
from datetime import datetime
from datetime import timedelta


import pymysql
import tensorflow as tf
from flask import Flask
from flask import request 
from flask import Response
from flask import jsonify

import GCN.train_list1_pre as list1_pre
import GCN.train_list4_pre as list4_pre
import pre_inflow  as list3_pre
import GCN.train_time_pre as dettime_pre

app = Flask(__name__)
app.debug=True

class DB():
    
    def __init__(self, library="library_flow"):
        super().__init__()
        self.connect(library)

    def connect(self,DB):
        DB_USER = 'maker0'
        DB_PASS = 'Maker0000'
        DB_HOST = 'rm-bp11labi01950io698o.mysql.rds.aliyuncs.com'
        DB_PORT = 3306
        DATABASE = DB
        try:
            self.connect_info = pymysql.connect(user=DB_USER, passwd=DB_PASS, host=DB_HOST, port=DB_PORT, db=DATABASE, use_unicode=True, charset="utf8")  #1
            self.cursor = self.connect_info.cursor()
        except:
            print("连接失败")
        
    def close(self):
        self.connect_info.close()
db = DB('library_pre')
def parse_jsondata(data):
    # 现在是7:10分
    # ori_dict = {
    #     'time': 0,  
    #     'weather': None, 
    #     'dayprop': None, 
    #     'temperatures': None, 
    #     'station': {
    #         'name': 'Sta65',
    #         'flow': 0,
    #         'flow_type': 0, 
    #         'type': None, 
    #         'station_classify': None, 
    #     }
    # }
    #           time_start CHAR(20),
    #         weather CHAR(100),
    #         weather2 CHAR(100),
    #         dayprop INT,
    #         temperatures1 INT,
    #         temperatures2 INT,
    #         station CHAR(100),
    #         flow INT,
    #         flow_type INT,
    #         station_classify INT,
    #         id INT)"""
    lllll = [None for i in range(11)]
    ori_dict = {}
    weather_kinds = ['多云', '中雨', '阴', '晴', '雷阵雨', '暴雨', '大雨', '小雨']
    for key in data.keys():
        ori_dict[key] = data[key]
        if key == 'time':
            lllll[0] = data[key]
            a = "7:1:7:21"
            b = data[key]
            a = datetime.strptime(a, "%m:%d:%H:%M")  # Y m d  H M S 
            b = datetime.strptime(b, "%m:%d:%H:%M")  # Y m d  H M S 
            tomorrow = b + timedelta(days=1)
            days = (b-a).days
            seconds = (b-a).seconds
            det = int(days*32 + seconds/60/30)
            ori_dict[key] = [det, int(seconds/60/30), a, b]
        elif key == 'weather':
            lllll[1] = data[key][0]
            lllll[2] = data[key][1]
            a = []
            weather_kind = [0,0,0,0,0,0,0,0]
            weather_kind[weather_kinds.index(data[key][0])] = 1
            a.extend(weather_kind)
            weather_kind = [0,0,0,0,0,0,0,0]
            weather_kind[weather_kinds.index(data[key][1])] = 1
            a.extend(weather_kind)
            ori_dict[key] = a
        elif key == 'dayprop':
            lllll[3] = int(data[key])
            ori_dict[key] = data[key]
        elif key == 'temperatures':
            lllll[4] = int(data[key][0])
            lllll[5] = int(data[key][1])
            ori_dict[key] = data[key]
        elif key == 'station':
            ori_dict[key] = {}
            dict2 = data[key]
            ori_dict[key]['name'] = dict2['name']
            lllll[6] = dict2['name']
            if 'flow' in dict2.keys():
                lllll[7] = int(dict2['flow'][0])
                lllll[8] = int(dict2['flow'][1])
                ori_dict[key]['flow'] = dict2['flow']
            if 'type' in dict2.keys():
                lllll[9] = int(dict2['type'])
                ori_dict[key]['type'] = dict2.get('type', 0)
            if 'station_classify' in dict2.keys():
                lllll[10] = int(dict2['station_classify'])
                a = [0,0,0,0,0]
                a[dict2.get('station_classify', 0)] = 1
                ori_dict[key]['station_classify'] = a
    lllll = tuple(lllll)
    db.cursor.execute(f'INSERT INTO input_records (time_start, weather1, weather2, dayprop, temperatures1, temperatures2, station, flow, flow_type, station_type, station_classify) VALUES {lllll}')
    db.connect_info.commit()
    db.cursor.execute('SELECT MAX(id) from input_records')
    id = db.cursor.fetchone()
    id = id[0]
    print('最大的主键: ', id)
    return ori_dict, id

@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='*'
    return environ

@app.route('/python/get', methods=['GET'])
def hello_world():
    return 'hello world'

@app.route('/python/getJson', methods=['GET'])
def hello_world1():
    result = {
        'msg': 'hello world',
        'students': [
            {
                "id": 1,
                "name": '张三'
            }, {
                'id': 2,
                'name': '李四'
            }
        ] 
    }
    return jsonify(result)

@app.route('/python/post', methods=['POST'])
def post():
    data = request.get_json()
    username = data['username']
    password = data['password']
    result = {
        'username': username,
        'password': password
    }
    return jsonify(result)

@app.route('/python/postSearch', methods=['POST'])
def post1():
    data = request.get_json()
    username = data['username']
    password = data['password']
    print(username, password)
    result = {
        'username': username,
        'password': password
    }
    return jsonify(result)


@app.route('/python/predict', methods=['POST'])
def pre():
    print('-'*50)
    data = request.get_json()
    print(data)
    if data != None:
        data, id = parse_jsondata(data)
    else:
        print('无参数请求')
        data = {}
    # 加载模型并预测
    try:
        model = list1_pre.load_model()
        list1 = list1_pre.predict_web(model, data)
        db.cursor.executemany('INSERT INTO list1_predict VALUES(%s,%s,%s,%s,%s,%s,%s)', [[a['station'], a['flow'][0], a['flow'][1], a['flow'][2], a['flow'][3], a['turn'], id] for a in list1])
        model = list4_pre.load_model()
        list1 = list4_pre.predict_web(model, data)         
        db.cursor.executemany('INSERT INTO list4_predict VALUES(%s,%s,%s,%s)', [[a['line'], a['flow'], a['turn'], id] for a in list1])
        model = list3_pre.load_model()
        list1 = list3_pre.predict_web(model, data)
        db.cursor.executemany('INSERT INTO list3_predict VALUES(%s,%s,%s,%s,%s)', [ [str(a['station1']), str(a['station1']), int(a['flow']), int(a['turn']), int(id)] for a in list1])
        db.connect_info.commit()
        msg = 'success'
    except:
        msg = 'error'
    return_dict = {
        'msg': msg,
        # 'data': {
        #     'list1': str(list1),
        #     'list4': str(list4),
        #     'list3': str(list3),
        # }
    }
    print('')
    return jsonify(return_dict)

@app.route('/python/list1', methods=['POST'])
def pre_list1():
    print('-'*50)
    data = request.get_json()
    print(data)
    if data != None:
        data, id = parse_jsondata(data)
    else:
        print('无参数请求')
        data = {}
    # 加载模型并预测
    try:
        model = list1_pre.load_model()
        list1 = list1_pre.predict_web(model, data)
        db.cursor.executemany('INSERT INTO list1_predict VALUES(%s,%s,%s,%s,%s,%s,%s)', [[a['station'], a['flow'][0], a['flow'][1], a['flow'][2], a['flow'][3], a['turn'], id] for a in list1])
        db.connect_info.commit()
        msg = 'success'
    except:
        msg = 'error'
    return_dict = {
        'msg': msg,
    }
    print('')
    return jsonify(return_dict)

@app.route('/python/list4', methods=['POST'])
def pre_list4():
    print('-'*50)
    data = request.get_json()
    print(data)
    if data != None:
        data, id = parse_jsondata(data)
    else:
        data = {}
        print('无参数请求')
        pass
    # 加载模型并预测

    try:
        model = list4_pre.load_model()
        list1 = list4_pre.predict_web(model, data)         
        db.cursor.executemany('INSERT INTO list4_predict VALUES(%s,%s,%s,%s)', [[a['line'], a['flow'], a['turn'], id] for a in list1])
        db.connect_info.commit()
        msg = 'success'
    except:
        msg = 'error'     
    return_dict = {
        'msg': msg,
    }
    print('')
    return jsonify(return_dict)

@app.route('/python/list3', methods=['POST'])
def pre_list3():
    print('-'*50)
    data = request.get_json()
    print(data)
    if data != None:
        data, id = parse_jsondata(data)
    else:
        data = {}
        print('无参数请求')
    # 加载模型并预测
    try:
        model = list3_pre.load_model()
        list1 = list3_pre.predict_web(model, data)
        db.cursor.executemany('INSERT INTO list3_predict VALUES(%s,%s,%s,%s,%s)', [ [str(a['station1']), str(a['station1']), int(a['flow']), int(a['turn']), int(id)] for a in list1])
        db.connect_info.commit()
        msg = 'success'
    except:
        msg = 'error'
    return_dict = {
        'msg': msg,
    }
    print('')
    return jsonify(return_dict)

@app.route('/python/dettime', methods=['POST'])
def dettime():
    data = request.get_json()
    model = dettime_pre.load_model()
    dettime = dettime_pre.predict(model, data)
    return_dict = {
        'dettime': int(dettime),
        'msg': '嘿嘿嘿'
    }
    return jsonify(return_dict)

if __name__ == '__main__':
    # models = load_models()
    print("-----------模型加载完成-----------")
    app.run(host='localhost',port=9999)
