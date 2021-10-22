import numpy as np
# import tensorflow as tf
# from tensorflow.keras.layers import Dense, SimpleRNN, Dropout, GRU, LSTM, Embedding
# import matplotlib.pyplot as plt
import os
import datetime
import pandas as pd
import sklearn.preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
# from tensorflow.keras.utils import to_categorical
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
# print(daily_flow.shape)
sc = MinMaxScaler(feature_range=(0,1))
daily_flow_scaled = sc.fit_transform(np.array(daily_flow))
# print(daily_flow_scaled)

x_train_1, y_train_1 = [], []
x_train, y_train = [], []

for route, sta, dist, anyday, dayprop, month, day, flow in zip(route_onehot, sta_onehot, dist_onehot, anydays, dayprop_onehot, np.array(df['month']), np.array(df['day']), np.array(daily_flow_scaled)):
    x_arr = list(route) + list(sta) + list(dist) + list(dayprop) + [int(anyday), month, day]
    y_arr = flow[0]
    x_train_1.append(x_arr)
    y_train_1.append(y_arr)
    # print(x_arr)
    # print(y_arr)
    # break
    print(len(x_arr))
    print(len(route),' ', len(sta),' ', len(dist),' ', anyday,' ', len(dayprop),' ', month,' ', day,' ', flow )