import numpy as np
# import tensorflow as tf
# from tensorflow.keras.layers import Dense, GRU, Dropout, GRU, GRU, Embedding
import matplotlib.pyplot as plt
import os
import datetime
import pandas as pd
# import sklearn.preprocessing
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.metrics import mean_squared_error, mean_absolute_error
# from tensorflow.keras.utils import to_categorical
print('正在处理输入数据')
# 1. 导入原始数据
year = 2020
station = pd.DataFrame(pd.read_csv('./data/station.csv', encoding='gbk'))
workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
df = pd.DataFrame(pd.read_csv('./sta_flow_by_day.csv'))

df = df.loc[df['sta']=='Sta65']

# 星期几
anydays = []
for month, day in zip(np.array(df['month']), np.array(df['day'])):
    anyday=datetime.datetime(year,month,day).strftime("%w");
    anydays.append(anyday)
df['anyday'] = anydays
df_1 = df.sort_values(by=['anyday','flow'])
plt.figure()
plt.plot(np.array(df_1['flow']))
# plt.plot(np.array(range(len(df_1['flow'])), np.array(df_1['flow']))

# 6.是否放假 onehot
workday['date'] = pd.to_datetime(workday['Column1'],format="%Y%m%d")
dayprops = []
for month, day in zip(np.array(df['month']), np.array(df['day'])):
    dayprop = np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]
    # dayprop = int(float((np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]).strip())) 
    dayprops.append(dayprop) 
df['dayprop'] = dayprops
df_2 = df.sort_values(by=['dayprop','flow'])
plt.figure()
plt.plot(np.array( df_2['flow']))
# plt.xticks(range(len(dayprops)), dayprops, rotation=270)

df_3 = df.sort_values(by=['day','flow'])
plt.figure()
plt.plot(np.array( df_3['flow']))

print(np.array(dayprops).shape)
print(np.array(df['flow']).shape)
# plt.plot()
plt.show()
