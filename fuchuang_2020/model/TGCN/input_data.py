# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 15:15:50 2018

@author: Administrator
"""

import numpy as np
import pandas as pd
import pickle as pkl

# def load_sz_data(dataset):
#     sz_adj = pd.read_csv(r'data/sz_adj.csv',header=None)
#     adj = np.mat(sz_adj)
#     sz_tf = pd.read_csv(r'data/sz_speed.csv')
#     print(sz_tf.shape, adj.shape)
#     return sz_tf, adj

def load_sz_data():
    # sz_adj = pd.read_csv(r'data/list1_G.csv',header=None)
    sz_adj = pd.read_csv(r'data/list3_G.csv',header=None)
    adj = np.mat(sz_adj)
    # sz_tf = pd.read_csv(r'data/list1_in_flow.csv',header=None)
    sz_tf = pd.read_csv(r'data/list3_flow.csv',header=None, dtype=np.float16)
    # sz_tf = pd.read_csv(r'data/a1.csv',header=None)
    print(sz_tf.shape, adj.shape)
    return sz_tf.iloc[:], adj

def load_data_partly():
    sz_adj = pd.read_csv(r'data/list3_G.csv',header=None)
    adj = np.mat(sz_adj)
    sz_tf = pd.read_csv(r'data/list3_flow.csv',header=None, dtype=np.float16)
    batch = int(len(sz_tf)/800)
    aaa = []
    aaa.append(sz_tf.iloc[:800+12])
    for i in range(1, batch):
        aaa.append(sz_tf.iloc[800*i:800*(i+1)+12])
    aaa.append(sz_tf.iloc[800*(i+1):])
    len_sum = 0
    for a in aaa:
        len_sum += len(a)
    print('总长度', len_sum)
    return aaa, adj

def only_test_data(data, time_len):
    re = []
    for i in range(len(data)-time_len):
        re.append(data[i:i+time_len])
    re = np.array(re)
    return re

def only_test_data_nearest(data, time_len):
    re = []
    # for i in range(len(data)-time_len):
    re.append(data[-time_len:])
    re = np.array(re)
    return re


def preprocess_data(data, time_len, rate, seq_len, pre_len):

    train_size = int(time_len * rate)
    train_data = data[0:train_size]
    test_data = data[train_size:time_len]
    trainX, trainY, testX, testY = [], [], [], []
    for i in range(len(train_data) - seq_len - pre_len):
        a = train_data[i: i + seq_len + pre_len]
        trainX.append(a[0 : seq_len])
        trainY.append(a[seq_len : seq_len + pre_len])
    for i in range(len(test_data) - seq_len -pre_len):
        b = test_data[i: i + seq_len + pre_len]
        testX.append(b[0 : seq_len])
        testY.append(b[seq_len : seq_len + pre_len])
    
    trainX1 = np.array(trainX)
    trainY1 = np.array(trainY)
    testX1 = np.array(testX)
    testY1 = np.array(testY)
    return trainX1, trainY1, testX1, testY1
    
