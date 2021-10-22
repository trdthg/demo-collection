# -*- coding: utf-8 -*-

import os
import time

import pickle as pkl
import pandas as pd
import numpy as np
import numpy.linalg as la
import tensorflow as tf
import matplotlib.pyplot as plt
import pymysql

try:
    import Process.dijkstra as dijkstra
except:
    pass


try:
    import input_data
    from input_data import preprocess_data, load_sz_data, load_data_partly, only_test_data, only_test_data_nearest
    from tgcn2 import tgcnCell
    from visualization2 import plot_result,plot_error
except:
    import TGCN.input_data as input_data
    from TGCN.input_data import preprocess_data, load_sz_data, load_data_partly, only_test_data, only_test_data_nearest
    from TGCN.tgcn2 import tgcnCell
    from TGCN.visualization2 import plot_result,plot_error
station_order = [(49.0, 65.0), (65.0, 49.0), (149.0, 49.0), (49.0, 149.0), (74.0, 149.0), (149.0, 74.0), (128.0, 74.0), (74.0, 128.0), (34.0, 128.0), (128.0, 34.0), (106.0, 34.0), (34.0, 106.0), (110.0, 106.0), (106.0, 110.0), (97.0, 110.0), (110.0, 97.0), (80.0, 97.0), (97.0, 80.0), (89.0, 80.0), (80.0, 89.0), (64.0, 89.0), (136.0, 89.0), (137.0, 89.0), (89.0, 64.0), (150.0, 64.0), (64.0, 150.0), (154.0, 150.0), (150.0, 154.0), (107.0, 154.0), (154.0, 107.0), (83.0, 107.0), (107.0, 83.0), (108.0, 83.0), (83.0, 108.0), (47.0, 108.0), (18.0, 47.0), (123.0, 47.0), (47.0, 159.0), (1.0, 159.0), (159.0, 1.0), (129.0, 63.0), (3.0, 63.0), (25.0, 63.0), (63.0, 129.0), (9.0, 129.0), (129.0, 9.0), (163.0, 9.0), (9.0, 163.0), (53.0, 163.0), (163.0, 53.0), (79.0, 53.0), (53.0, 79.0), (18.0, 79.0), (79.0, 18.0), (47.0, 18.0), (47.0, 123.0), (127.0, 123.0), (123.0, 127.0), (81.0, 127.0), (91.0, 127.0), (60.0, 127.0), (127.0, 81.0), (27.0, 81.0), (81.0, 27.0), (48.0, 27.0), (27.0, 48.0), (151.0, 48.0), (48.0, 151.0), (68.0, 151.0), (151.0, 68.0), (52.0, 68.0), (68.0, 52.0), (76.0, 52.0), (52.0, 76.0), (57.0, 76.0), (76.0, 57.0), (71.0, 57.0), (57.0, 71.0), (139.0, 71.0), (71.0, 139.0), (105.0, 139.0), (139.0, 105.0), (51.0, 105.0), (105.0, 51.0), (24.0, 51.0), (51.0, 24.0), (156.0, 143.0), (143.0, 156.0), (61.0, 156.0), (156.0, 61.0), (50.0, 61.0), (61.0, 50.0), (119.0, 50.0), (50.0, 119.0), (66.0, 119.0), (119.0, 66.0), (12.0, 66.0), (66.0, 12.0), (161.0, 12.0), (12.0, 161.0), (21.0, 161.0), (161.0, 21.0), (133.0, 21.0), (21.0, 133.0), (22.0, 133.0), (133.0, 22.0), (138.0, 22.0), (22.0, 138.0), (41.0, 138.0), (138.0, 41.0), (30.0, 41.0), (32.0, 41.0), (91.0, 41.0), (41.0, 30.0), (67.0, 30.0), (30.0, 67.0), (144.0, 67.0), (67.0, 144.0), (29.0, 144.0), (144.0, 29.0), (126.0, 29.0), (29.0, 126.0), (115.0, 126.0), (126.0, 115.0), (40.0, 115.0), (118.0, 115.0), (162.0, 115.0), (115.0, 40.0), (131.0, 40.0), (40.0, 131.0), (39.0, 131.0), (131.0, 39.0), (100.0, 39.0), (39.0, 100.0), (135.0, 100.0), (100.0, 135.0), (167.0, 135.0), (168.0, 135.0), (134.0, 135.0), (135.0, 167.0), (113.0, 167.0), (167.0, 113.0), (141.0, 113.0), (113.0, 141.0), (142.0, 141.0), (141.0, 142.0), (158.0, 142.0), (142.0, 158.0), (44.0, 158.0), (158.0, 44.0), (117.0, 44.0), (44.0, 117.0), (147.0, 117.0), (117.0, 147.0), (42.0, 147.0), (147.0, 42.0), (35.0, 42.0), (42.0, 35.0), (87.0, 35.0), (35.0, 87.0), (109.0, 87.0), (88.0, 87.0), (94.0, 87.0), (87.0, 109.0), (33.0, 109.0), (109.0, 33.0), (112.0, 33.0), (33.0, 112.0), (153.0, 112.0), (112.0, 153.0), (125.0, 153.0), (153.0, 125.0), (121.0, 125.0), (125.0, 121.0), (11.0, 121.0), (121.0, 11.0), (114.0, 157.0), (157.0, 114.0), (168.0, 114.0), (162.0, 114.0), (15.0, 114.0), (114.0, 168.0), (135.0, 168.0), (135.0, 134.0), (85.0, 134.0), (90.0, 134.0), (95.0, 134.0), (134.0, 85.0), (2.0, 85.0), (85.0, 2.0), (4.0, 2.0), (2.0, 4.0), (103.0, 4.0), (4.0, 103.0), (145.0, 103.0), (103.0, 145.0), (88.0, 145.0), (145.0, 88.0), (87.0, 88.0), (87.0, 94.0), (160.0, 94.0), (94.0, 160.0), (7.0, 160.0), (160.0, 7.0), (6.0, 7.0), (7.0, 6.0), (8.0, 6.0), (6.0, 8.0), (75.0, 8.0), (8.0, 75.0), (102.0, 75.0), (45.0, 75.0), (152.0, 75.0), (75.0, 102.0), (84.0, 90.0), (26.0, 90.0), (134.0, 90.0), (90.0, 84.0), (59.0, 84.0), (84.0, 59.0), (19.0, 59.0), (59.0, 19.0), (62.0, 19.0), (19.0, 62.0), (165.0, 62.0), (62.0, 165.0), (38.0, 165.0), (165.0, 38.0), (58.0, 38.0), (38.0, 58.0), (10.0, 43.0), (43.0, 10.0), (96.0, 10.0), (10.0, 96.0), (132.0, 96.0), (96.0, 132.0), (37.0, 132.0), (132.0, 37.0), (16.0, 37.0), (37.0, 16.0), (69.0, 16.0), (16.0, 69.0), (54.0, 69.0), (69.0, 54.0), (56.0, 54.0), (23.0, 56.0), (118.0, 56.0), (75.0, 45.0), (75.0, 152.0), (164.0, 152.0), (152.0, 164.0), (82.0, 164.0), (164.0, 82.0), (111.0, 82.0), (82.0, 111.0), (140.0, 111.0), (99.0, 140.0), (140.0, 13.0), (70.0, 13.0), (13.0, 70.0), (55.0, 70.0), (70.0, 55.0), (20.0, 55.0), (55.0, 20.0), (23.0, 20.0), (20.0, 23.0), (56.0, 23.0), (17.0, 23.0), (26.0, 23.0), (56.0, 118.0), (115.0, 118.0), (115.0, 162.0), (114.0, 162.0), (114.0, 15.0), (86.0, 15.0), (95.0, 15.0), (72.0, 15.0), (15.0, 86.0), (46.0, 86.0), (86.0, 46.0), (3.0, 46.0), (46.0, 3.0), (63.0, 3.0), (93.0, 3.0), (92.0, 3.0), (63.0, 25.0), (146.0, 25.0), (25.0, 146.0), (130.0, 146.0), (146.0, 130.0), (120.0, 130.0), (130.0, 120.0), (122.0, 77.0), (77.0, 122.0), (36.0, 122.0), (122.0, 36.0), (28.0, 36.0), (36.0, 28.0), (124.0, 28.0), (28.0, 124.0), (166.0, 124.0), (124.0, 166.0), (99.0, 166.0), (166.0, 99.0), (140.0, 99.0), (89.0, 136.0), (89.0, 137.0), (101.0, 137.0), (137.0, 101.0), (31.0, 101.0), (101.0, 31.0), (17.0, 31.0), (31.0, 17.0), (23.0, 17.0), (23.0, 26.0), (90.0, 26.0), (134.0, 95.0), (15.0, 95.0), (15.0, 72.0), (93.0, 72.0), (72.0, 93.0), (3.0, 93.0), (3.0, 92.0), (116.0, 92.0), (92.0, 116.0), (32.0, 116.0), (116.0, 32.0), (41.0, 32.0), (41.0, 91.0), (127.0, 91.0), (127.0, 60.0), (148.0, 60.0), (60.0, 148.0), (73.0, 148.0), (148.0, 73.0), (108.0, 47.0), (159.0, 47.0), (54.0, 56.0), (111.0, 140.0), (13.0, 140.0)]

    
k = 1
train_rate =  0.
seq_len = 14 * k
output_dim = pre_len = 3 * k
gru_units = 128
modelpath = f"model/model_list3_{gru_units}_{k}.ckpt"

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
                        time_start CHAR(20) NOT NULL,
                        turn INT )"""
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
                        time_start CHAR(20) NOT NULL,
                        turn INT )"""
                sql4 = f'''CREATE TABLE IF NOT EXISTS {table_name_4}  (
                        linename CHAR(20) NOT NULL,
                        flow FLOAT,
                        time_start CHAR(20) NOT NULL,
                        turn INT )'''
                self.cursor.execute(sql1)
                # self.cursor.execute(sql2)
                self.cursor.execute(sql3)
                self.cursor.execute(sql4)
        except pymysql.Error as e:
            raise e
    
    def close(self):
        self.connect_info.close()

def load_model():
    os.environ['CUDA_VISIBLE_DEVICES']='2'
    ###### Settings ######
    

    a  = time.time()
    ###### load data ######
    print('-'*40, 'data_shape', '-'*40)
    # data, adj = load_sz_data()
    data, adj = load_data_partly()
    time_len = data[0].shape[0]  #2977
    num_nodes = data[0].shape[1] #156
    data1 =np.mat(data[0],dtype=np.float32)
    print(data1.shape)
    print(station_order.index((26.0, 90.0)))
    

    #### normalization
    max_value = np.max(data1)
    data1  = data1/max_value

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
    return [sess, y_pred, inputs, data, seq_len, pre_len]

def predict_web(qqq, info, a = True):
    print('-----list3-----')
    sess, y_pred, inputs, data, seq_len, pre_len = qqq[0],qqq[1],qqq[2],qqq[3],qqq[4],qqq[5]
    data1 = data[-1]
    data1 =np.mat(data1,dtype=np.float32)
    max_value = np.max(data1)
    data1  = data1/max_value
    for_predict_data = only_test_data_nearest(data1, seq_len)
    # max_value = np.max(for_predict_data)    
    aaa = for_predict_data   
    print(aaa.shape)
    if info and a:
        for key in info.keys():
            if key == 'time':
                pred = predict_web(qqq, info, False)
                print(pred.shape)
                aaa[0] = np.r_[aaa[0][3*k:], pred]
                # aaa[0] = pred[0][-406:]
                pass
            if key == 'station':
                name = info[key]['name']
                if 'flow' in info[key].keys():
                    g = []
                    sum_ = 0
                    b = []
                    near_stations = dijkstra.getNearStations(name)
                    for near_station in near_stations:
                        try:
                            head_index = 340-station_order.index((float(name[3:]), near_stations))
                            flow = aaa[-head_index]
                            g.append(flow)
                            sum_ += flow
                            b.append(head_index)
                        except:
                            pass
                    for i in range(len(g)):
                        aaa[-b[i]] += g[i] / sum_ * info[key]['flow']

    pred = sess.run([y_pred], feed_dict = {inputs:for_predict_data})
    pred = pred[0]
    if a:
        pred = pred * max_value
        pred = np.round(pred)
        print(pred.shape)
        data_for_web = []
        for i, list_flow in enumerate(pred):
            for j, station_tuple in enumerate(station_order):
                station1 = f'Sta{int(station_tuple[0])}'
                station2 = f'Sta{int(station_tuple[1])}'
                flow = list_flow[j]
                which_turn = int(j/4) + 1
                data_for_web.append({'station1':station1, 'station2':station2, 'flow':flow, 'turn':int(which_turn)})
        return data_for_web
    else: 
        return pred

def predict(aaa, info, a = True):
    
    sess, y_pred, inputs, data, seq_len, pre_len = aaa[0],aaa[1],aaa[2],aaa[3],aaa[4],aaa[5]
    predict = []
    for i, data1 in enumerate(data):
        print(i)
        data1 =np.mat(data1,dtype=np.float32)
        max_value = np.max(data1)
        data1  = data1/max_value
        for_predict_data = only_test_data(data1, seq_len)


        pred = sess.run([y_pred], feed_dict = {inputs:for_predict_data})
        pred = pred[0] * max_value
        # print(len(pred)/4)
        # print(type(pred))
        if predict != []:
            predict = np.r_[predict, pred]
        else:
            predict = pred
        print('predict.shape: ',predict.shape[0] / 4)
    return predict

def build_data_for_db(predict):
    # 把预测数据写入数据库中
    time_start_list = []
    for month in (3,4,5,6):
        for day in range(1, 30):
            # if (month==3 and day<12):
            #     continue
            for hour in range(6, 23):
                for minute in [0, 30]:
                    time_start_list.append(f'{month}-{day}:{hour}:{minute}')
    time_start_list = time_start_list[12:]
    print('len: ',len(time_start_list))
    # return

    station_order = [(49.0, 65.0), (65.0, 49.0), (149.0, 49.0), (49.0, 149.0), (74.0, 149.0), (149.0, 74.0), (128.0, 74.0), (74.0, 128.0), (34.0, 128.0), (128.0, 34.0), (106.0, 34.0), (34.0, 106.0), (110.0, 106.0), (106.0, 110.0), (97.0, 110.0), (110.0, 97.0), (80.0, 97.0), (97.0, 80.0), (89.0, 80.0), (80.0, 89.0), (64.0, 89.0), (136.0, 89.0), (137.0, 89.0), (89.0, 64.0), (150.0, 64.0), (64.0, 150.0), (154.0, 150.0), (150.0, 154.0), (107.0, 154.0), (154.0, 107.0), (83.0, 107.0), (107.0, 83.0), (108.0, 83.0), (83.0, 108.0), (47.0, 108.0), (18.0, 47.0), (123.0, 47.0), (47.0, 159.0), (1.0, 159.0), (159.0, 1.0), (129.0, 63.0), (3.0, 63.0), (25.0, 63.0), (63.0, 129.0), (9.0, 129.0), (129.0, 9.0), (163.0, 9.0), (9.0, 163.0), (53.0, 163.0), (163.0, 53.0), (79.0, 53.0), (53.0, 79.0), (18.0, 79.0), (79.0, 18.0), (47.0, 18.0), (47.0, 123.0), (127.0, 123.0), (123.0, 127.0), (81.0, 127.0), (91.0, 127.0), (60.0, 127.0), (127.0, 81.0), (27.0, 81.0), (81.0, 27.0), (48.0, 27.0), (27.0, 48.0), (151.0, 48.0), (48.0, 151.0), (68.0, 151.0), (151.0, 68.0), (52.0, 68.0), (68.0, 52.0), (76.0, 52.0), (52.0, 76.0), (57.0, 76.0), (76.0, 57.0), (71.0, 57.0), (57.0, 71.0), (139.0, 71.0), (71.0, 139.0), (105.0, 139.0), (139.0, 105.0), (51.0, 105.0), (105.0, 51.0), (24.0, 51.0), (51.0, 24.0), (156.0, 143.0), (143.0, 156.0), (61.0, 156.0), (156.0, 61.0), (50.0, 61.0), (61.0, 50.0), (119.0, 50.0), (50.0, 119.0), (66.0, 119.0), (119.0, 66.0), (12.0, 66.0), (66.0, 12.0), (161.0, 12.0), (12.0, 161.0), (21.0, 161.0), (161.0, 21.0), (133.0, 21.0), (21.0, 133.0), (22.0, 133.0), (133.0, 22.0), (138.0, 22.0), (22.0, 138.0), (41.0, 138.0), (138.0, 41.0), (30.0, 41.0), (32.0, 41.0), (91.0, 41.0), (41.0, 30.0), (67.0, 30.0), (30.0, 67.0), (144.0, 67.0), (67.0, 144.0), (29.0, 144.0), (144.0, 29.0), (126.0, 29.0), (29.0, 126.0), (115.0, 126.0), (126.0, 115.0), (40.0, 115.0), (118.0, 115.0), (162.0, 115.0), (115.0, 40.0), (131.0, 40.0), (40.0, 131.0), (39.0, 131.0), (131.0, 39.0), (100.0, 39.0), (39.0, 100.0), (135.0, 100.0), (100.0, 135.0), (167.0, 135.0), (168.0, 135.0), (134.0, 135.0), (135.0, 167.0), (113.0, 167.0), (167.0, 113.0), (141.0, 113.0), (113.0, 141.0), (142.0, 141.0), (141.0, 142.0), (158.0, 142.0), (142.0, 158.0), (44.0, 158.0), (158.0, 44.0), (117.0, 44.0), (44.0, 117.0), (147.0, 117.0), (117.0, 147.0), (42.0, 147.0), (147.0, 42.0), (35.0, 42.0), (42.0, 35.0), (87.0, 35.0), (35.0, 87.0), (109.0, 87.0), (88.0, 87.0), (94.0, 87.0), (87.0, 109.0), (33.0, 109.0), (109.0, 33.0), (112.0, 33.0), (33.0, 112.0), (153.0, 112.0), (112.0, 153.0), (125.0, 153.0), (153.0, 125.0), (121.0, 125.0), (125.0, 121.0), (11.0, 121.0), (121.0, 11.0), (114.0, 157.0), (157.0, 114.0), (168.0, 114.0), (162.0, 114.0), (15.0, 114.0), (114.0, 168.0), (135.0, 168.0), (135.0, 134.0), (85.0, 134.0), (90.0, 134.0), (95.0, 134.0), (134.0, 85.0), (2.0, 85.0), (85.0, 2.0), (4.0, 2.0), (2.0, 4.0), (103.0, 4.0), (4.0, 103.0), (145.0, 103.0), (103.0, 145.0), (88.0, 145.0), (145.0, 88.0), (87.0, 88.0), (87.0, 94.0), (160.0, 94.0), (94.0, 160.0), (7.0, 160.0), (160.0, 7.0), (6.0, 7.0), (7.0, 6.0), (8.0, 6.0), (6.0, 8.0), (75.0, 8.0), (8.0, 75.0), (102.0, 75.0), (45.0, 75.0), (152.0, 75.0), (75.0, 102.0), (84.0, 90.0), (26.0, 90.0), (134.0, 90.0), (90.0, 84.0), (59.0, 84.0), (84.0, 59.0), (19.0, 59.0), (59.0, 19.0), (62.0, 19.0), (19.0, 62.0), (165.0, 62.0), (62.0, 165.0), (38.0, 165.0), (165.0, 38.0), (58.0, 38.0), (38.0, 58.0), (10.0, 43.0), (43.0, 10.0), (96.0, 10.0), (10.0, 96.0), (132.0, 96.0), (96.0, 132.0), (37.0, 132.0), (132.0, 37.0), (16.0, 37.0), (37.0, 16.0), (69.0, 16.0), (16.0, 69.0), (54.0, 69.0), (69.0, 54.0), (56.0, 54.0), (23.0, 56.0), (118.0, 56.0), (75.0, 45.0), (75.0, 152.0), (164.0, 152.0), (152.0, 164.0), (82.0, 164.0), (164.0, 82.0), (111.0, 82.0), (82.0, 111.0), (140.0, 111.0), (99.0, 140.0), (140.0, 13.0), (70.0, 13.0), (13.0, 70.0), (55.0, 70.0), (70.0, 55.0), (20.0, 55.0), (55.0, 20.0), (23.0, 20.0), (20.0, 23.0), (56.0, 23.0), (17.0, 23.0), (26.0, 23.0), (56.0, 118.0), (115.0, 118.0), (115.0, 162.0), (114.0, 162.0), (114.0, 15.0), (86.0, 15.0), (95.0, 15.0), (72.0, 15.0), (15.0, 86.0), (46.0, 86.0), (86.0, 46.0), (3.0, 46.0), (46.0, 3.0), (63.0, 3.0), (93.0, 3.0), (92.0, 3.0), (63.0, 25.0), (146.0, 25.0), (25.0, 146.0), (130.0, 146.0), (146.0, 130.0), (120.0, 130.0), (130.0, 120.0), (122.0, 77.0), (77.0, 122.0), (36.0, 122.0), (122.0, 36.0), (28.0, 36.0), (36.0, 28.0), (124.0, 28.0), (28.0, 124.0), (166.0, 124.0), (124.0, 166.0), (99.0, 166.0), (166.0, 99.0), (140.0, 99.0), (89.0, 136.0), (89.0, 137.0), (101.0, 137.0), (137.0, 101.0), (31.0, 101.0), (101.0, 31.0), (17.0, 31.0), (31.0, 17.0), (23.0, 17.0), (23.0, 26.0), (90.0, 26.0), (134.0, 95.0), (15.0, 95.0), (15.0, 72.0), (93.0, 72.0), (72.0, 93.0), (3.0, 93.0), (3.0, 92.0), (116.0, 92.0), (92.0, 116.0), (32.0, 116.0), (116.0, 32.0), (41.0, 32.0), (41.0, 91.0), (127.0, 91.0), (127.0, 60.0), (148.0, 60.0), (60.0, 148.0), (73.0, 148.0), (148.0, 73.0), (108.0, 47.0), (159.0, 47.0), (54.0, 56.0), (111.0, 140.0), (13.0, 140.0)]
    data_for_db = {month:[] for month in [1,2,3,4,5,6,7,8,9,10,11,12]}
    for i, list_flow in enumerate(predict):
        print(i, len(list_flow))
        for j, station_tuple in enumerate(station_order):
            station1 = f'Sta{int(station_tuple[0])}'
            station2 = f'Sta{int(station_tuple[1])}'
            flow = list_flow[j]
            which_turn = j%4 + 1
            time_start = time_start_list[int((i+0.1)/4)]
            data_for_db[int(time_start.split("-")[0])].append([station1, station2, float(flow), time_start.split("-")[1], int(which_turn)])
    return data_for_db

def write_to_db(data):
    db = DB('library_flow')
    for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
        print(month)
        # table_name_1 = f'list1_predict_{month}'
        # table_name_2 = f'list2_predict'
        table_name_3 = f'list3_predict_{month}'
        # table_name_4 = f'list4_predict_{month}'
        db.cursor.executemany(f'INSERT INTO {table_name_3} VALUES(%s,%s,%s,%s,%s)', data[month])
        db.connect_info.commit()

def main():
    # db = DB('library_flow')
    model = load_model()
    
    # predict(aaa, data, seq_len, pre_len)
    predict_web(model, {})
    # write_to_db(data)


if __name__ == '__main__':
    main()

