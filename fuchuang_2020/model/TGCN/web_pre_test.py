#!/usr/bin/python3
import sys
import json
import time
import socket


import numpy as np
import matplotlib.pyplot as plt
import demjson


# print("启动")
# # 创建 socket 对象
# s = socket.socket(
#             socket.AF_INET, socket.SOCK_STREAM) 
# # 获取本地主机名
# host = socket.gethostname()
# port = 9999
# # 绑定端口号
# s.bind((host, port))
# # 设置最大连接数，超过后排队
# s.listen(5)

# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import pickle as pkl
import pandas as pd
import numpy as np
import numpy.linalg as la
import tensorflow as tf
import matplotlib.pyplot as plt
import pymysql

try:
    from TGCN.input_data import preprocess_data,load_sz_data
    from TGCN.tgcn2 import tgcnCell
    from TGCN.visualization2 import plot_result,plot_error
except:
    from input_data import preprocess_data,load_sz_data
    from tgcn2 import tgcnCell
    from visualization2 import plot_result,plot_error
    
class DB():
    
    def __init__(self, DB):
        DB_USER = 'maker0'
        DB_PASS = 'Maker0000'
        DB_HOST = 'rm-bp11labi01950io698o.mysql.rds.aliyuncs.com'
        DB_PORT = 3306
        DATABASE = DB
        try:
            self.connect_info = pymysql.connect(user=DB_USER, passwd=DB_PASS, host=DB_HOST, port=DB_PORT, db=DATABASE)  #1
            self.cursor = self.connect_info.cursor()
            for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
                table_name_1 = f'list1_predict_{month}'
                # table_name_2 = f'list2_predict'
                table_name_3 = f'list3_predict_{month}'
                table_name_4 = f'list4_predict_{month}'
                sql1 = f"""CREATE TABLE IF NOT EXISTS {table_name_1} (
                        station  CHAR(20) NOT NULL,
                        in_flow FLOAT,
                        out_flow FLOAT,
                        in_flow_plus FLOAT,
                        out_flow_plus FLOAT,
                        time_start CHAR(20) NOT NULL )"""
                # sql2 = f"""CREATE TABLE IF NOT EXISTS {table_name_2} (
                #         station_in  CHAR(20) NOT NULL,
                #         station_out  CHAR(20) NOT NULL,
                #         flow FLOAT,
                #         flow_plus FLOAT,
                #         time_start CHAR(20) NOT NULL )"""
                sql3 = f"""CREATE TABLE IF NOT EXISTS {table_name_3} (
                        station_1  CHAR(20) NOT NULL,
                        station_2  CHAR(20) NOT NULL,
                        flow FLOAT,
                        time_start CHAR(20) NOT NULL )"""
                sql4 = f'''CREATE TABLE IF NOT EXISTS {table_name_4}  (
                        linename CHAR(20) NOT NULL,
                        flow FLOAT,
                        time_start CHAR(20) NOT NULL )'''
                self.cursor.execute(sql1)
                # self.cursor.execute(sql2)
                self.cursor.execute(sql3)
                self.cursor.execute(sql4)
        except pymysql.Error as e:
            raise e
    
    def close(self):
        self.connect_info.close()

def msg_process(msg, test):
    msg = demjson.encode(demjson.decode(msg)).encode('utf-8').decode('unicode_escape')
    print(msg, type(msg)) 
    # print("连接地址: %s" % str(c_addr))
    data='欢迎访问菜鸟教程！'+ "\r\n"
    msg = dict(json.loads(msg))
    print(msg, type(msg))
    
    weather_kinds = ['多云', '中雨', '阴', '晴', '雷阵雨', '暴雨', '大雨', '小雨']
    for key in msg.keys():
        if key == 'weather':
            a = [0, 0, 0, 0, 0, 0, 0, 0]
            for b in msg[key]:
                a[weather_kinds.index(b)] = 1
            msg[key] = a
        elif key == 'temperatures':
            pass
    return msg
    
def load_model():
    db = DB('library_flow')
    ###### Settings ######
    modelpath = "model/model_list3_128.ckpt"
    train_rate =  0.
    seq_len = 12
    output_dim = pre_len = 4
    gru_units = 128

    ###### load data ######
    print('-'*40, 'data_shape', '-'*40)
    data, adj = load_sz_data()
    print(data.shape)
    time_len = data.shape[0]  #2977
    num_nodes = data.shape[1] #156
    data1 =np.mat(data,dtype=np.float32)
    print(data1.shape)

    #### normalization
    max_value = np.max(data1)
    data1  = data1/max_value
    trainX, trainY, testX, testY = preprocess_data(data1, time_len, train_rate, seq_len, pre_len)
    print('trainX', trainX.shape)
    print('trainY', trainY.shape)
    print('testX', testX.shape, type(testX))
    print('testY', testY.shape)
    training_data_count = len(trainX)

    def TGCN(_X, _weights, _biases):
        ###
        cell_1 = tgcnCell(gru_units, adj, num_nodes=num_nodes)
        cell = tf.compat.v1.nn.rnn_cell.MultiRNNCell([cell_1], state_is_tuple=True)
        _X = tf.unstack(_X, axis=1)
        outputs, states = tf.compat.v1.nn.static_rnn(cell, _X, dtype=tf.float32)
        m = []
        for i in outputs:
            o = tf.reshape(i,shape=[-1,num_nodes,gru_units])
            o = tf.reshape(o,shape=[-1,gru_units])
            m.append(o)
        last_output = m[-1]
        output = tf.matmul(last_output, _weights['out']) + _biases['out']
        output = tf.reshape(output,shape=[-1,num_nodes,pre_len])
        output = tf.transpose(a=output, perm=[0,2,1])
        output = tf.reshape(output, shape=[-1,num_nodes])
        return output, m, states
            
    ###### placeholders ######
    tf.compat.v1.disable_eager_execution()
    inputs = tf.compat.v1.placeholder(tf.float32, shape=[None, seq_len, num_nodes], name='inputs')
    labels = tf.compat.v1.placeholder(tf.float32, shape=[None, pre_len, num_nodes], name='labels')

    # Graph weights
    weights = {
        'out': tf.Variable(tf.random.normal([gru_units, pre_len], mean=1.0), name='weight_o')}
    biases = {
        'out': tf.Variable(tf.random.normal([pre_len]),name='bias_o')}
    pred,ttts,ttto = TGCN(inputs, weights, biases)
    y_pred = pred

    ###### optimizer ######
    lambda_loss = 0.0015
    Lreg = lambda_loss * sum(tf.nn.l2_loss(tf_var) for tf_var in tf.compat.v1.trainable_variables())
    label = tf.reshape(labels, [-1,num_nodes])
    ###### Initialize session ######
    variables = tf.compat.v1.global_variables()
    saver = tf.compat.v1.train.Saver(tf.compat.v1.global_variables()) 
    #sess = tf.Session()
    gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.333)
    sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))
    sess.run(tf.compat.v1.global_variables_initializer())
    saver.restore(sess, modelpath)
    return [sess, y_pred, inputs, testX]
# pred = sess.run([y_pred], feed_dict = {inputs:testX})
# pred = pred[0]
def predict_web(aaa, info):
    sess, y_pred, inputs, testX = aaa[0],aaa[1],aaa[2],aaa[3],
    # sess, y_pred, inputs, testX = load_model()

    pred = sess.run([y_pred], feed_dict = {inputs:testX})
    pred = pred[0]
    print(pred.shape)
    return pred[0]

feature_index_dict = {
    'month': [0],
    'dayprop': [1],
    'anyday': [2],
    'hour':[3],
    'noon':[4],
    'weather': [5,6],
    'temperatures': [7,8],
    'station_classify':[9,10,11,12,13],
}

def main():
    sess, y_pred, inputs, testX = load_model()
    # pred = sess.run([y_pred], feed_dict = {inputs:testX})
    # print(pred[0].shape)

if __name__ == '__main__':
    main()