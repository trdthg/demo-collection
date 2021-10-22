# -*- coding: utf-8 -*-
import os
import math
import time

import pickle as pkl
import pandas as pd
import numpy as np
import numpy.linalg as la
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error,mean_absolute_error

from input_data import preprocess_data,load_sz_data
from tgcn2 import tgcnCell
from visualization2 import plot_result,plot_error

time_start = time.time()
###### Settings ######
train_rate =  0.80
k = 29
seq_len = 14*k
output_dim = pre_len = 3*k
batch_size = 32
lr = 0.0001
training_epoch = 1
gru_units = 128
modelpath = f"model/model_list3_{gru_units}_{k}.ckpt"

###### load data ######
print('-'*40, 'data_shape', '-'*40)
data, adj = load_sz_data()
print(data.shape)
time_len = data.shape[0]  #2977
num_nodes = data.shape[1] #156
data1 =np.mat(data)
print(data1.shape)

#### normalization
max_value = np.max(data1)
data1  = data1/max_value
trainX, trainY, testX, testY = preprocess_data(data1, time_len, train_rate, seq_len, pre_len)
print('trainX', trainX.shape)
print('trainY', trainY.shape)
print('testX', testX.shape)
print('testY', testY.shape)
totalbatch = int(trainX.shape[0]/batch_size)
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
##loss
loss = tf.reduce_mean(input_tensor=tf.nn.l2_loss(y_pred-label) + Lreg)
##rmse
error = tf.sqrt(tf.reduce_mean(input_tensor=tf.square(y_pred-label)))
optimizer = tf.compat.v1.train.AdamOptimizer(lr).minimize(loss)

###### Initialize session ######
variables = tf.compat.v1.global_variables()
saver = tf.compat.v1.train.Saver(tf.compat.v1.global_variables()) 
#sess = tf.Session()
gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=0.333)
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))
sess.run(tf.compat.v1.global_variables_initializer())
saver.restore(sess, modelpath)

###### evaluation ######
def evaluation(a,b):
    rmse = math.sqrt(mean_squared_error(a,b))
    mae = mean_absolute_error(a, b)
    F_norm = la.norm(a-b,'fro')/la.norm(a,'fro')
    r2 = 1-((a-b)**2).sum()/((a-a.mean())**2).sum()
    var = 1-(np.var(a-b))/np.var(a)
    return rmse, mae, 1-F_norm, r2, var
 
   
x_axe,batch_loss,batch_rmse,batch_pred = [], [], [], []
test_loss,test_rmse,test_mae,test_acc,test_r2,test_var,test_pred = [],[],[],[],[],[],[]
SAVE_FILE = modelpath
for epoch in range(training_epoch):
    print(f'epoch: {epoch}')
    for m in range(totalbatch):
        mini_batch = trainX[m * batch_size : (m+1) * batch_size]
        mini_label = trainY[m * batch_size : (m+1) * batch_size]
        _, loss1, rmse1, train_output = sess.run([optimizer, loss, error, y_pred],
                                                 feed_dict = {inputs:mini_batch, labels:mini_label})
        batch_loss.append(loss1)
        batch_rmse.append(rmse1 * max_value)
     # Test completely at every epoch
    loss2, rmse2, test_output = sess.run([loss, error, y_pred],
                                         feed_dict = {inputs:testX, labels:testY})
    test_label = np.reshape(testY,[-1,num_nodes])
    
    rmse, mae, acc, r2_score, var_score = evaluation(test_label, test_output)
    test_label1 = test_label * max_value
    test_output1 = test_output * max_value
    test_loss.append(loss2)
    test_rmse.append(rmse * max_value)
    test_mae.append(mae * max_value)
    test_acc.append(acc)
    test_r2.append(r2_score)
    test_var.append(var_score)
    test_pred.append(test_output1)
    
    print('Iter:{}'.format(epoch),
          'train_rmse:{:.4}'.format(batch_rmse[-1]),
          'test_loss:{:.4}'.format(loss2),
          'test_rmse:{:.4}'.format(rmse),
          'test_acc:{:.4}'.format(acc))
    
    # if (epoch % 500 == 0):        
    #     saver.save(sess, path+'/model_100/TGCN_pre_%r'%epoch, global_step = epoch)

savepath = saver.save(sess,SAVE_FILE)

time_end = time.time()
print(time_end-time_start,'s')

############## visualization ###############
b = int(len(batch_rmse)/totalbatch)
batch_rmse1 = [i for i in batch_rmse]
train_rmse = [(sum(batch_rmse1[i*totalbatch:(i+1)*totalbatch])/totalbatch) for i in range(b)]
batch_loss1 = [i for i in batch_loss]
train_loss = [(sum(batch_loss1[i*totalbatch:(i+1)*totalbatch])/totalbatch) for i in range(b)]

index = test_rmse.index(np.min(test_rmse))
# test_result = test_pred[index]
# var = pd.DataFrame(test_result)
# var.to_csv(path+'/test_result.csv',index = False,header = False)
#plot_result(test_result,test_label1,path)
#plot_error(train_rmse,train_loss,test_rmse,test_acc,test_mae,path)

print('min_rmse:%r'%(np.min(test_rmse)),
      'min_mae:%r'%(test_mae[index]),
      'max_acc:%r'%(test_acc[index]),
      'r2:%r'%(test_r2[index]),
      'var:%r'%test_var[index])

############## predict ###############

pred = sess.run([y_pred], feed_dict = {inputs:testX})
pred = pred[0]
y = []
print(np.array(testY).shape)
print(np.array(pred).shape)
pred = pred[::4]
for v in testY:
    y.append(v[0][0] * max_value)
x = []
for v in pred:
    # print(len(v))
    x.append(v[0] * max_value)
y = list(y)
x = list(x)
print('x',x)
print('y',y)
plt.figure()
plt.plot(x)
plt.plot(y)
try:
    plt.figure()
    plt.plot(train_loss)
    plt.plot(test_loss)
except:
    pass
plt.show()
print(len(x))
print(len(y))

