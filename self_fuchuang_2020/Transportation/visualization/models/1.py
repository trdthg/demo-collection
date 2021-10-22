import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, SimpleRNN, Dropout, GRU, LSTM
import matplotlib.pyplot as plt
import os
import datetime
import pandas as pd
import sklearn.preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.utils import to_categorical
print('正在处理输入数据')
# 1. 导入原始数据
year = 2020
station = pd.DataFrame(pd.read_csv('./data/station.csv', encoding='gbk'))
workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
df = pd.DataFrame(pd.read_csv('./sta_flow_by_day.csv'))
# print(df)

# route. sta. dist. 星期几. 是否放假. 票价(不管). 

# 2. 把route列转为onehot编码
routes = []
for sta in np.array(df['sta']):
    route = np.array(station.loc[station['站点名称']==sta]['线路'])
    # print(route)
    routes.append(str(route))
enc_route = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
route_onehot = enc_route.fit_transform(np.array(routes).reshape(len(df['sta']),1))
# print(len(route_onehot))

# 3. 将sta转为onehot编码
enc_sta = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
sta_onehot = enc_sta.fit_transform(np.array(df['sta']).reshape(len(df['sta']),1))
# print(sta_onehot)

# 4. 将dist转为onehot编码
dists = []
for sta in np.array(df['sta']):
    dist = np.array(station.loc[station['站点名称']==sta]['行政区域'])
    dists.append(str(dist))
enc_dist = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
dist_onehot = enc_dist.fit_transform(np.array(dists).reshape(len(df['sta']),1))
# print(sta_onehot)

# 5. 星期几
anydays = []
for month, day in zip(np.array(df['month']), np.array(df['day'])):
    anyday=datetime.datetime(year,month,day).strftime("%w");
    anydays.append(anyday)
# print(anydays)
 
# 6.是否放假 onehot
workday['date'] = pd.to_datetime(workday['Column1'],format="%Y%m%d")
dayprops = []
for month, day in zip(np.array(df['month']), np.array(df['day'])):
    dayprop = np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]
    # dayprop = int(float((np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]).strip())) 
    dayprops.append(dayprop)
enc_dayprop = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
dayprop_onehot = enc_dayprop.fit_transform(np.array(dayprops).reshape(len(df['sta']),1))
# print(dayprop_onehot)


# 7. 将每月流量进行归一化处理
daily_flow = df.iloc[:, 3:4].values
print(daily_flow.shape)
sc = MinMaxScaler(feature_range=(0,1))
daily_flow_scaled = sc.fit_transform(np.array(daily_flow))
# print(daily_flow_scaled)

x_train, y_train = [], []

for route, sta, dist, anyday, dayprop, month, day, flow in zip(route_onehot, sta_onehot, dist_onehot, anydays, dayprop_onehot, np.array(df['month']), np.array(df['day']), np.array(daily_flow_scaled)):
    x_arr =  list(route) + list(sta) + list(dist) + list(dayprop) + [int(anyday), month, day]
    y_arr = flow[0]
    x_train.append(x_arr)
    y_train.append(y_arr)
    # print(x_arr)ss
    # print(y_arr)
    print(len(route),' ', len(sta),' ', len(dist),' ', anyday,' ', len(dayprop),' ', month,' ', day,' ', )
    # break
# print(x_train)


np.random.shuffle(x_train)
np.random.shuffle(y_train)

x_train, y_train = np.array(x_train), np.array(y_train)
# x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
print(x_train.shape)

print("正在搭建模型")
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(x_train.shape[1], 50),
    tf.keras.layers.Flatten(),
    # GRU(3, return_sequences=True),
    # GRU(1),
    # tf.keras.layers.Dense(512, activation='relu'),
    # tf.keras.layers.Dense(256, activation='relu'),
    # tf.keras.layers.Dense(256, activation='relu'),
    # # Dense(0.2),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    # Dense(0.1),
    # tf.keras.layers.Dense(64, activation='relu'),
    # tf.keras.layers.Dense(64, activation='relu'),
    # tf.keras.layers.Dense(32, activation='relu'),
    # tf.keras.layers.Dense(32, activation='relu'),
    # Dense(0.2),
    # tf.keras.layers.Dense(16, activation='relu'),
    # tf.keras.layers.Dense(16, activation='relu'),
    # tf.keras.layers.Dense(8, activation='relu'),
    # tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(1)
    # tf.keras.layers.Dense(64, activation='relu',kernel_regularizer=tf.keras.regularizers.l2()),
])

model.compile(
    optimizer = tf.keras.optimizers.Adam(0.001),
    # optimizer = tf.keras.optimizers.Adadelta(),
    loss = tf.keras.losses.mean_squared_error,
)

# checkpoint_save_path = './savedata/stockflow_month.ckpt'
# if os.path.exists(checkpoint_save_path + '.index'):
#     print('-----------------load the model------------------')
#     model.load_weights(checkpoint_save_path)

# cp_callback = tf.keras.callbacks.ModelCheckpoint(
#     filepath = checkpoint_save_path,
#     save_weights_only = True,
#     save_best_only = True,
#     # monitor = 'var_loss', # 指定需要监测的值
# )
print("正在训练")
history = model.fit(
    x_train, y_train,
    batch_size=16, epochs=30,
    validation_split=0.2,
    validation_freq=1,
    # callbacks = [cp_callback],
)

model.summary()      

# # 测试
# x_arr = list(route) + list(sta) + list(dist) + list(dayprop) + [int(anyday), month, day]

# route = ['1号线']
# sta = ['Sta1']
# route_onehot = enc_route.transform(np.array(route).reshape(len(route),1))
# sta_onehot = enc_sta.transform(np.array(sta).reshape(len(sta),1))
# sta_onehot = enc_sta.transform(np.array(sta).reshape(len(sta),1))
# x_test = []
# for route, sta in zip(route_onehot, sta_onehot):
#     x_arr = list(route) + list(sta)
#     x_test.append(x_arr)
# x_test = np.array(x_test)
# predict = model.predict(x_test)
# tf.print(predict)
# predict = sc.inverse_transform(predict)
# print(predict)


# loss = history.history['loss']
# val_loss = history.history['val_loss']

# plt.figure()
# plt.plot([1,2,3,4,5,6,7,8,9,10,11,12], predict[0] ,c='r')
# plt.plot([1,2,3,4,5,6,7,8,9,10,11,12], [896,45,381,861,1640,1358,334,0,0,0,0,40] ,c='b')

# plt.figure()
# plt.plot(loss, label='Training Loss')
# plt.plot(val_loss, label='Validation Loss')
# plt.title('Training and Validation Loss')
# plt.legend()

# plt.show()

print("正在处理测试数据")
#    '4号线': ['Sta59', 'Sta19', 'Sta62', 'Sta165', 'Sta58', 'Sta38', 'Sta84'], 
#    '5号线': ['Sta43', 'Sta10', 'Sta96', 'Sta132', 'Sta37', 'Sta16', 'Sta69', 'Sta54'], 
df = df.loc[df['sta']=='Sta65']
# print(df)

# 2. 把route列转为onehot编码
routes = []
for sta in np.array(df['sta']):
    route = np.array(station.loc[station['站点名称']==sta]['线路'])
    # print(route)
    routes.append(str(route))
# enc_route = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
route_onehot = enc_route.transform(np.array(routes).reshape(len(df['sta']),1))
# print(len(route_onehot))

# 3. 将sta转为onehot编码
# enc_sta = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
sta_onehot = enc_sta.transform(np.array(df['sta']).reshape(len(df['sta']),1))
# print(sta_onehot)

# 4. 将dist转为onehot编码
dists = []
for sta in np.array(df['sta']):
    dist = np.array(station.loc[station['站点名称']==sta]['行政区域'])
    dists.append(str(dist))
# enc_dist = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
dist_onehot = enc_dist.transform(np.array(dists).reshape(len(df['sta']),1))
# print(sta_onehot)

# 5. 星期几
anydays = []
for month, day in zip(np.array(df['month']), np.array(df['day'])):
    anyday=datetime.datetime(year,month,day).strftime("%w");
    anydays.append(anyday)
# print(anydays)
 
# 6.是否放假 onehot
workday['date'] = pd.to_datetime(workday['Column1'],format="%Y%m%d")
dayprops = []
for month, day in zip(np.array(df['month']), np.array(df['day'])):
    dayprop = np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]
    # dayprop = int(float((np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]).strip())) 
    dayprops.append(dayprop)
dayprop_onehot = enc_dayprop.transform(np.array(dayprops).reshape(len(df['sta']),1))
# print(dayprop_onehot)


# 7. 将每月流量进行归一化处理
daily_flow = df.iloc[:, 3:4].values
daily_flow_scaled = sc.transform(daily_flow)
# print(daily_flow_scaled)

x_train, y_train = [], []

for route, sta, dist, anyday, dayprop, month, day, flow in zip(route_onehot, sta_onehot, dist_onehot, anydays, dayprop_onehot, np.array(df['month']), np.array(df['day']),np.array(daily_flow_scaled)):
    x_arr = list(route) + list(sta) + list(dist) + list(dayprop) + [int(anyday), month, day]
    y_arr = flow[0]
    x_train.append(x_arr)
    y_train.append(y_arr)
    # print(len(x_arr))
    # print(len(route),' ', len(sta),' ', len(dist),' ', anyday,' ', len(dayprop),' ', month,' ', day,' ', flow )
# print(x_train.shape)

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1]))
print(np.array(x_train).shape)

predict = []
predict_ori = model.predict(x_train)
print(predict_ori.shape)
# print(predict_ori)
print(predict_ori.shape)

predict = sc.inverse_transform(predict_ori)
print(predict.shape)
print("开始做图")

df = pd.DataFrame(pd.read_csv('./sta_flow_by_day.csv'))
i=0
plt.figure()
for sta in np.array(station.loc[station['线路']=='1号线']['站点名称']):
    i+=1
    # plt.figure()
    if sta=='Sta65':
        print(sta)
        df_ = df.loc[(df['sta'] == sta)]
        x = range(0, len(np.array(df_['month'])))
        X = [str(f'{month}.{day}') for month, day in zip(np.array(df_['month']), np.array(df_['day']))]
        Y = np.array(df_['flow'])
        plt.plot( x,Y, label=sta)
        plt.xticks(range(len(X)), X, rotation=270)
        plt.legend()
        break
# plt.figure()
plt.plot( predict, c='r', label='PREDICT')
plt.xticks(range(len(X)), X, rotation=270)
plt.legend()


loss = history.history['loss']
val_loss = history.history['val_loss']
plt.figure()
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()


















