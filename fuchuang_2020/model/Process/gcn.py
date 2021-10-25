
import time
import csv

import pymysql
import numpy as np
import scipy.sparse as sp
import pandas as pd
import networkx as nx
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import activations, regularizers, constraints, initializers
from sklearn.metrics import accuracy_score

import graph 
import shortestpass
from pyasn1.type.univ import Null

lr = 0.01
dropout = 0
verbose = 1
epochs = 30
weight_decay = 5e-4


class PreProcess():

    def __init__(self):
        super().__init__()
        print('-'*100)
        self.dbconnect("library_flow")
        reader = shortestpass.ReadFile()
        self.all_stations = reader.readTxt()

    def dbconnect(self,DB):
        DB_USER = 'maker0'
        DB_PASS = 'Maker0000'
        DB_HOST = 'rm-bp11labi01950io698o.mysql.rds.aliyuncs.com'
        DB_PORT = 3306
        DATABASE = DB
        try:
            self.connect_info = pymysql.connect(user=DB_USER, passwd=DB_PASS, host=DB_HOST, port=DB_PORT, db=DATABASE)  #1
            self.cursor = self.connect_info.cursor()
        except:
            print("连接失败")

    def getGraph(self):
        # 1. 得到 A (所有节点的邻接矩阵)
        graph_dict = {}
        for this_line in self.all_stations:
            for station in this_line:
                graph_dict[float(station.getName()[3:])] = []
                result = station.getNearStations(station)
                for near_station in result:
                    if near_station != Null:
                        graph_dict[float(station.getName()[3:])].append(float(near_station.getName()[3:]))
        self.graph_dict = graph_dict
        print(graph_dict.keys())
        G=nx.Graph(graph_dict)
        # print(G.nodes.data())
        G_mat = nx.adjacency_matrix(G)
        print(type(G_mat))
        print(G_mat.toarray())
        with open('G.csv','w',newline='') as f3:
            f3_csv = csv.writer(f3)
            f3_csv.writerows(G_mat.toarray())
        print('G.shape', G_mat.shape)
        # nx.draw(G,with_labels=True,node_size=50,node_color='r',width=0.1,edge_color='r',font_color=None,font_size=6)
        # plt.show()
        return G

    def getFlow(self, time_len=12, test_len=4):
        workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
        workday['date'] = pd.to_datetime(workday['Column1'],format="%Y%m%d")
        # 2. 得到 X (特征矩阵)

        # x_train为进站流量信息, y_train包含了[进站流量, 线路流量, 断面流量]
        # 故一个batch要以一个时段的进站流量为单位
        x_train, y_train = [], []
        for day in range(1, 3):
            # 得到是否是节假日
            dayprop = np.array(workday.loc[(workday['date'].dt.month==6) & (workday['date'].dt.day==day)]['Column2'])[0]
            print('dayprop', dayprop)
            for hour in range(7, 22):
                for minute in range(0, 2):
                    x_train_part, y_train_part = [], []

                    time_start = f'{day}:{hour}:{30*minute}'
                    sql = f'SELECT station, in_flow_plus FROM list1_6 WHERE time_start = "{time_start}"'
                    self.cursor.execute(sql)
                    # 获取某一时段的流量原始数据
                    a = self.cursor.fetchall()
                    sql = f'SELECT linename, flow FROM list4_6 WHERE time_start = "{time_start}"'
                    self.cursor.execute(sql)
                    # 获取某一时段的流量原始数据
                    b = self.cursor.fetchall()
                    lineflow = []
                    for linename in ['1号线','2号线','3号线','4号线','5号线','10号线','11号线','12号线']:
                        for row_of_b in b:
                            if row_of_b[0] == linename:
                                lineflow.append(row_of_b[1])
                    
                        # 封装为邻接矩阵形式
                    # dict_, list_ = {}, []
                    already_in_stations = []
                    staflow = []

                    x_train_dict, y_train_dict = {}, {}
                    for row in a:
                        already_in_stations.append(row[0])
                        # dict_[row[0]] = [row[0], hour, minute, row[1]]
                        x_train_dict[float(row[0][3:])] = [float(row[0][3:]), hour, minute*30, dayprop, row[1]]
                        # y_train_dict[float(row[0][3:])] = [row[1]]
                    for key in [65.0, 49.0, 149.0, 74.0, 128.0, 34.0, 106.0, 110.0, 97.0, 80.0, 89.0, 64.0, 150.0, 154.0, 107.0, 83.0, 108.0, 47.0, 159.0, 1.0, 63.0, 129.0, 9.0, 163.0, 53.0, 79.0, 18.0, 123.0, 127.0, 81.0, 27.0, 48.0, 151.0, 68.0, 52.0, 76.0, 57.0, 71.0, 139.0, 105.0, 51.0, 24.0, 143.0, 156.0, 61.0, 50.0, 119.0, 66.0, 12.0, 161.0, 21.0, 133.0, 22.0, 138.0, 41.0, 30.0, 67.0, 144.0, 29.0, 126.0, 115.0, 40.0, 131.0, 39.0, 100.0, 135.0, 167.0, 113.0, 141.0, 142.0, 158.0, 44.0, 117.0, 147.0, 42.0, 35.0, 87.0, 109.0, 33.0, 112.0, 153.0, 125.0, 121.0, 11.0, 157.0, 114.0, 168.0, 134.0, 85.0, 2.0, 4.0, 103.0, 145.0, 88.0, 94.0, 160.0, 7.0, 6.0, 8.0, 75.0, 102.0, 90.0, 84.0, 59.0, 19.0, 62.0, 165.0, 38.0, 58.0, 43.0, 10.0, 96.0, 132.0, 37.0, 16.0, 69.0, 54.0, 56.0, 45.0, 152.0, 164.0, 82.0, 111.0, 140.0, 13.0, 70.0, 55.0, 20.0, 23.0, 118.0, 162.0, 15.0, 86.0, 46.0, 3.0, 25.0, 146.0, 130.0, 120.0, 77.0, 122.0, 36.0, 28.0, 124.0, 166.0, 99.0, 136.0, 137.0, 101.0, 31.0, 17.0, 26.0, 95.0, 72.0, 93.0, 92.0, 116.0, 32.0, 91.0, 60.0, 148.0, 73.0]:
                        x_train.append(x_train_dict.get(key, [key, hour, minute*30, dayprop, 0.]))
                        # y_train.append(y_train_dict.get(key, [0.]))
                    # print(x_train)
                    # print(y_train)

                    # with open('x_train.csv','w',newline='') as f3:
                    #     f3_csv = csv.writer(f3)
                    #     f3_csv.writerows(x_train)
                    # with open('y_train.csv','w',newline='') as f3:
                    #     f3_csv = csv.writer(f3)
                    #     f3_csv.writerows(y_train)



        with open('cq_flow.csv','w',newline='') as f3:
            f3_csv = csv.writer(f3)
            rows = []
            for i in range(len(x_train)-time_len-test_len):
                rows.append(x_train[i:i+time_len+test_len])
            f3_csv.writerows(rows)

                    
            #         break
            #     break
            # break
        print('-'*100)
        print('len(x,y _train)', len(y_train), len(x_train))
        return [x_train, y_train]

    def get_part_flow(self, time_len=12, test_len=4):
        workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
        workday['date'] = pd.to_datetime(workday['Column1'],format="%Y%m%d")
        # 2. 得到 X (特征矩阵)

        # x_train为进站流量信息, y_train包含了[进站流量, 线路流量, 断面流量]
        # 故一个batch要以一个时段的进站流量为单位
        x_train, y_train = [], []
        for day in range(1, 3):
            # 得到是否是节假日
            dayprop = np.array(workday.loc[(workday['date'].dt.month==6) & (workday['date'].dt.day==day)]['Column2'])[0]
            print('dayprop', dayprop)
            for hour in range(7, 22):
                for minute in range(0, 2):
                    x_train_part, y_train_part = [], []

                    time_start = f'{day}:{hour}:{30*minute}'
                    sql = f'SELECT station, in_flow_plus FROM list1_6 WHERE time_start = "{time_start}"'
                    self.cursor.execute(sql)
                    # 获取某一时段的流量原始数据
                    a = self.cursor.fetchall()
                    sql = f'SELECT linename, flow FROM list4_6 WHERE time_start = "{time_start}"'
                    self.cursor.execute(sql)
                    # 获取某一时段的流量原始数据
                    b = self.cursor.fetchall()
                    lineflow = []
                    for linename in ['1号线','2号线','3号线','4号线','5号线','10号线','11号线','12号线']:
                        for row_of_b in b:
                            if row_of_b[0] == linename:
                                lineflow.append(row_of_b[1])
                    
                        # 封装为邻接矩阵形式
                    # dict_, list_ = {}, []
                    already_in_stations = []
                    staflow = []

                    x_train_dict, y_train_dict = {}, {}
                    for row in a:
                        already_in_stations.append(row[0])
                        # dict_[row[0]] = [row[0], hour, minute, row[1]]
                        x_train_dict[float(row[0][3:])] = [float(row[0][3:]), hour, minute*30, dayprop, row[1]]
                        # y_train_dict[float(row[0][3:])] = [row[1]]
                    for key in [65.0, 49.0, 149.0, 74.0, 128.0, 34.0, 106.0, 110.0, 97.0, 80.0, 89.0, 64.0, 150.0, 154.0, 107.0, 83.0, 108.0, 47.0, 159.0, 1.0, 63.0, 129.0, 9.0, 163.0, 53.0, 79.0, 18.0, 123.0, 127.0, 81.0, 27.0, 48.0, 151.0, 68.0, 52.0, 76.0, 57.0, 71.0, 139.0, 105.0, 51.0, 24.0, 143.0, 156.0, 61.0, 50.0, 119.0, 66.0, 12.0, 161.0, 21.0, 133.0, 22.0, 138.0, 41.0, 30.0, 67.0, 144.0, 29.0, 126.0, 115.0, 40.0, 131.0, 39.0, 100.0, 135.0, 167.0, 113.0, 141.0, 142.0, 158.0, 44.0, 117.0, 147.0, 42.0, 35.0, 87.0, 109.0, 33.0, 112.0, 153.0, 125.0, 121.0, 11.0, 157.0, 114.0, 168.0, 134.0, 85.0, 2.0, 4.0, 103.0, 145.0, 88.0, 94.0, 160.0, 7.0, 6.0, 8.0, 75.0, 102.0, 90.0, 84.0, 59.0, 19.0, 62.0, 165.0, 38.0, 58.0, 43.0, 10.0, 96.0, 132.0, 37.0, 16.0, 69.0, 54.0, 56.0, 45.0, 152.0, 164.0, 82.0, 111.0, 140.0, 13.0, 70.0, 55.0, 20.0, 23.0, 118.0, 162.0, 15.0, 86.0, 46.0, 3.0, 25.0, 146.0, 130.0, 120.0, 77.0, 122.0, 36.0, 28.0, 124.0, 166.0, 99.0, 136.0, 137.0, 101.0, 31.0, 17.0, 26.0, 95.0, 72.0, 93.0, 92.0, 116.0, 32.0, 91.0, 60.0, 148.0, 73.0]:
                        x_train.append(x_train_dict.get(key, [key, hour, minute*30, dayprop, 0.]))
                        # y_train.append(y_train_dict.get(key, [0.]))
                    # print(x_train)
                    # print(y_train)

                    # with open('x_train.csv','w',newline='') as f3:
                    #     f3_csv = csv.writer(f3)
                    #     f3_csv.writerows(x_train)
                    # with open('y_train.csv','w',newline='') as f3:
                    #     f3_csv = csv.writer(f3)
                    #     f3_csv.writerows(y_train)

        with open('cq_flow.csv','w',newline='') as f3:
            f3_csv = csv.writer(f3)
            rows = []
            for i in range(len(x_train)-time_len-test_len):
                rows.append(x_train[i:i+time_len+test_len])
            f3_csv.writerows(rows)

                    
            #         break
            #     break
            # break
        print('-'*100)
        print('len(x,y _train)', len(y_train), len(x_train))
        return [x_train, y_train]

    def getData(self):
        G = self.getGraph()
        result = self.getFlow()
        A_mat = nx.adjacency_matrix(G)
        X_mat = np.array(result[0])
        # print(result[0][0])
        # print(result[1][1][0])
        # 暂时以单站流量作为y
        z_vec = np.array(result[1])
        train_idx = range(len(X_mat))
        val_idx = range(len(X_mat)-20, len(X_mat))
        return [A_mat, X_mat, z_vec, train_idx, val_idx]

class GCNConv(tf.keras.layers.Layer):
    # # 定义图卷积层
    def __init__(self, units,
                 activation=lambda x: x,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 **kwargs):
        super(GCNConv, self).__init__()

        self.units = units
        print('units', units, type(units))
        self.activation = activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.bias_initializer = initializers.get(bias_initializer)

    def build(self, input_shape):
        """ GCN has two inputs : [shape(An), shape(X)]
        """
        print('input_shape', input_shape, type(input_shape))
        fdim = input_shape[1][1]  # feature dim
        print('fdim', fdim, type(fdim))
        # 初始化权重矩阵
        self.weight = self.add_weight(name="weight",
                                      shape=(fdim, self.units),
                                      initializer=self.kernel_initializer,
                                      trainable=True)
        if self.use_bias:
            # 初始化偏置项
            self.bias = self.add_weight(name="bias",
                                        shape=(self.units, ),
                                        initializer=self.bias_initializer,
                                        trainable=True)

    def call(self, inputs):
        """ GCN has two inputs : [An, X]
        """
        
        # print('input', inputs, type(inputs))
        # print('input0', type(inputs[0]))  shape=(2708， 2708)  稀疏矩阵 (13264, 2) values_shape=(13264,)  
        # print('input1', type(inputs[1]))  [2708 1433] and shape=(2708, 16)
        # return  
        # inputs 是 weight  tensor类型
        self.An = inputs[0]  # （稀疏邻接矩阵
        self.X = inputs[1]   #  
        # 计算 XW
        if isinstance(self.X, tf.SparseTensor):
            h = tf.sparse.sparse_dense_matmul(self.X, self.weight)
        else:
            h = tf.matmul(self.X, self.weight)
        # 计算 AXW
        output = tf.sparse.sparse_dense_matmul(self.An, h)

        if self.use_bias:
            output = tf.nn.bias_add(output, self.bias)

        if self.activation:
            output = self.activation(output)

        return output

class GCN():
    # # 定义GCN模型
    def __init__(self, An, X, sizes, **kwargs):
        self.with_relu = True
        self.with_bias = True

        self.lr = lr
        self.dropout = dropout
        self.verbose = verbose
        
        self.An = An  # 邻接矩阵
        self.X = X    # 特征矩阵
        self.layer_sizes = sizes  # [隐藏层神经元个数, 输出类别数]
        self.shape = An.shape     # An 的形状
        print('An', self.shape, type(An))
        print('X', X.shape, type(X))
        self.An_tf = sp_matrix_to_sp_tensor(self.An)  # 稀疏矩阵转为完整张量 -> w
        self.X_tf = tf.convert_to_tensor(self.X, dtype=tf.float32)    #  同上


        # 定义两个Layer层 
        self.layer1 = GCNConv(self.layer_sizes[0], activation='relu')  #第一层的形状是输入 特征矩阵 的shape
        self.layer2 = GCNConv(self.layer_sizes[1])   # 第二层的输入为第一层的输出 
        self.opt = tf.optimizers.Adam(learning_rate=self.lr)

    def train(self, idx_train, labels_train, idx_val, labels_val):
        print('-'*50, 'train','-'*50)
        # K = np.int64((labels_train.max() + 1))
        K = np.int64(1)
        print("-"*50)
        print(K, type(K), K.shape)
        train_losses = []
        val_losses = []
        # use adam to optimize
        for it in range(epochs):
            tic = time.time()
            with tf.GradientTape() as tape:
                print('idx_train',idx_train)
                print('labels_train',labels_train,labels_train.shape)
                # _loss = self.loss_fn(idx_train, np.eye(K)[labels_train.astype('int64')])
                _loss = self.loss_fn(idx_train, labels_train)

            # optimize over weights
            print('_loss', _loss)
            grad_list = tape.gradient(_loss, self.var_list)
            grads_and_vars = zip(grad_list, self.var_list)
            self.opt.apply_gradients(grads_and_vars)

            # evaluate on the training
            train_loss = self.evaluate(idx_train, labels_train, training=True)
            print("什么鬼")
            train_losses.append(train_loss)
            val_loss = self.evaluate(idx_val, labels_val, training=False)
            val_losses.append(val_loss)
            toc = time.time()
            if self.verbose:
                print(it, 'train_loss', train_loss, 'val_loss', val_loss)
        return train_losses, val_losses

    def loss_fn(self, idx, labels, training=True):
        print('-'*50, 'loss_fn','-'*50)
        if training:
            # .nnz 是获得X中元素的个数
            # _X = sparse_dropout(self.X_tf, self.dropout, [self.X.nnz])
            # _X = sparse_dropout(self.X_tf, self.dropout, [self.X.shape[0] * self.X.shape[1]])
            _X = sparse_dropout(self.X_tf, self.dropout, [self.X.size])
        else:
            _X = self.X_tf
        
        self.h1 = self.layer1([self.An_tf, _X])
        if training:
            _h1 = tf.nn.dropout(self.h1, self.dropout)
        else:
            _h1 = self.h1

        self.h2 = self.layer2([self.An_tf, _h1])
        print('-'*50)
        print('self.h2', self.h2.shape, type(self.h2))
        self.var_list = self.layer1.weights + self.layer2.weights
        # calculate the loss base on idx and labels
        # tf.gather根据所给的索引进行切片
        _logits = tf.gather(self.h2, idx)
        _losses = 0
        for a,b in zip(labels, _logits):
            _losses += (a-b)**2

        _loss = _losses/len(labels)
        # _loss_per_node = tf.nn.compute_average_loss(labels=labels, logits=_logits)

        # _loss_per_node = tf.reduce_mean(labels=labels, logits=_logits)

        # print('_loss_per_node', _loss_per_node, type(_loss_per_node), _loss_per_node.shape)
        # _loss = tf.reduce_mean(_loss_per_node)
        # print('_loss', _loss, type(_loss))
        # # 加上 l2 正则化项
        # _loss += weight_decay * sum(map(tf.nn.l2_loss, self.layer1.weights))


        print('_loss', _loss, type(_loss))
        return _loss

    def evaluate(self, idx, true_labels, training):
        print('-'*50, 'evaluate','-'*50)
        K = true_labels.max() + 1
        # _loss = self.loss_fn(idx, np.eye(K)[true_labels], training=training).numpy()
        _loss = self.loss_fn(idx, true_labels)
        # _pred_logits = tf.gather(self.h2, idx)
        # _pred_labels = tf.argmax(_pred_logits, axis=1).numpy()
        # _acc = accuracy_score(_pred_labels, true_labels)
        return _loss


def sp_matrix_to_sp_tensor(M):
    # 稀疏矩阵转稀疏张量

    if not isinstance(M, sp.csr.csr_matrix):
        M = M.tocsr()
    # 获取非0元素坐标
    row, col = M.nonzero()
    # SparseTensor参数：二维坐标数组，数据，形状
    # 创建稀疏张量
    X = tf.SparseTensor(np.mat([row, col]).T, M.data, M.shape)
    X = tf.cast(X, tf.float32)
    return X

def sparse_dropout(x, dropout_rate, noise_shape):
    # 稀疏矩阵的 dropout
    # random_tensor = 1 - dropout_rate
    # random_tensor += tf.random.uniform(noise_shape)
    # dropout_mask = tf.cast(tf.floor(random_tensor), dtype=tf.bool)
    # # 从稀疏矩阵中取出dropout_mask对应的元素
    # print(type(x))
    # pre_out = tf.sparse.retain(x, dropout_mask)
    # return pre_out * (1. / (1 - dropout_rate))
    return x

def preprocess_graph(adj):
    # 计算标准化的邻接矩阵：根号D * A * 根号D
    # _A = A + I
    _adj = adj + sp.eye(adj.shape[0])   # 对角线原本全为0 现在全加上1
    # _dseq：各个节点的度构成的列表
    # (A_mat -> adj )coo_matrix.sum()返回一个np.matrix,并不是相加  np.matrix.A1返回一个flatten的np.array
    _dseq = _adj.sum(1).A1
    print('_desq', _dseq, len(_dseq))
    # 构造开根号的度矩阵
    _D_half = sp.diags(np.power(_dseq, -0.5))
    # 计算标准化的邻接矩阵, @ 表示矩阵乘法
    adj_normalized = _D_half @ _adj @ _D_half
    return adj_normalized.tocsr()

def main():

    db = PreProcess()
    A_mat, X_mat, z_vec, train_idx, val_idx = db.getData()
    An_mat = preprocess_graph(A_mat)
    K = 1  # 共有8种输出结果

    # 传入   邻接矩阵,特征矩阵 [隐藏层个数,  分类数量]
    model = GCN(An_mat, X_mat, [256, K])
    # 训练
    losses = model.train(train_idx, z_vec[train_idx], val_idx, z_vec[val_idx])

    for a, b in zip(losses[0], losses[1]):
        print(a, b)
    plt.plot(losses[0], label='train')
    plt.plot(losses[1], label='val')
    plt.show()
    # test_res = model.evaluate(test_idx, z_vec[test_idx], training=False)
    
if __name__ == "__main__":
    main()


