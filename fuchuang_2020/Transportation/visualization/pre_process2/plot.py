
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, GRU, Dropout, GRU, GRU, Embedding
import matplotlib.pyplot as plt
import os
import datetime
import pandas as pd
import sklearn.preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.utils import to_categorical

year = 2020
station = pd.DataFrame(pd.read_csv('./data/station.csv', encoding='gbk'))
workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
df = pd.DataFrame(pd.read_csv('./sta_flow_by_day.csv'))
# df = df.loc[df['sta']=='Sta65']


# for sta in np.array(station['站点名称']):
for sta in np.array(station.loc[station['线路']=='1号线']['站点名称']):
    if sta != 'Sta65':
        continue
    print(sta)
    df_ = df.loc[(df['sta'] == sta)]
    # x = range(0, len(np.array(df_['month'])))[15:]
    X = [str(f'{month}.{day}') for month, day in zip(np.array(df_['month']), np.array(df_['day']))]
    Y = np.array(df_['flow'])
    plt.plot( Y, label=sta)
    plt.xticks(range(len(X)), X, rotation=270)
    plt.legend()
plt.show()