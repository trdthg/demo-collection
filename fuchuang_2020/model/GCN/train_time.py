import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, GRU, Dropout, GRU, LSTM, Embedding
import matplotlib.pyplot as plt
import os
import datetime
import pandas as pd
import sklearn.preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.utils import to_categorical

def dataProcess():
    print('正在处理输入数据')
    # 1. 导入原始数据
    year = 2020
    trips = pd.DataFrame(pd.read_csv('./data/trips.csv', encoding='gbk')).sort_values(by='进站时间').reset_index(drop=True)
    trips['det'] = ((pd.to_datetime(trips['出站时间'],format="%Y/%m/%d %H:%M") - pd.to_datetime(trips['进站时间'],format="%Y/%m/%d %H:%M")).dt.total_seconds()/60).astype(int)
    print(trips['det'])
    trips['进站时间'] = pd.to_datetime(trips['出站时间'],format="%Y/%m/%d %H:%M")
    trips['出站时间'] = pd.to_datetime(trips['出站时间'],format="%Y/%m/%d %H:%M")

    # dummies_a = pd.get_dummies(trips['进站名称'])
    # dummies_b = pd.get_dummies(trips['出站名称'])
    enc_sta = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
    dummies_a = enc_sta.fit_transform(np.array(trips['进站名称']).reshape(len(trips['进站名称']),1))
    dummies_b = enc_sta.transform(np.array(trips['出站名称']).reshape(len(trips['出站名称']),1))
    a = enc_sta.transform([['Sta65']])
    print(list(a[0]) + [1])
    # return 
    workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
    workday['date'] = pd.to_datetime(workday['Column1'],format="%Y%m%d")

    # print(sta_onehot)

    train_data = []
    oldmonth = 0
    oldday = 0
    i = 0
    for trip in trips.itertuples():
        id = trip[1]
        month = trip[3].month
        hour = trip[3].hour
        day = trip[3].day
        if month==oldmonth and oldday==day:
            pass
        else:
            print(i)
            dayprop = np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]
        stationin = list(dummies_a[i].reshape(-1))
        # print(stationin)
        stationout = list(dummies_b[i].reshape(-1))
        det = trip[-1]
        i +=1
        # print(det, type(det))
        train_data.append(stationin + stationout + [month, hour, dayprop, det])
        oldday, oldmonth = day, month
    train_data = np.array(train_data)
    # np.savetxt('data/train_time.csv', train_data, delimiter=',')
    return train_data

def train(train_data):
    trainX = train_data[:,:-1]
    trainY = train_data[:,-1]

    model = tf.keras.Sequential([
        # GRU(256, return_sequences=True),
        # Dropout(0.1),
        Dense(2048, activation='swish'),
        Dense(256, activation='swish'),
        Dense(1)
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(0.0001),
        # loss=tf.keras.losses.categorical_crossentropy,
        loss=tf.keras.losses.mean_squared_error,
    )

    checkpoint_save_path = "savedata/train_time.ckpt"

    if os.path.exists(checkpoint_save_path + '.index'):
        print('-----------------load the model---------------')
        model.load_weights(checkpoint_save_path)

    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath = checkpoint_save_path,
        save_weights_only = True,
        save_best_only = True,
    )

    print("开始训练")
    history = model.fit(
        trainX, trainY,
        batch_size=16, epochs=5,
        validation_split=0.1,
        validation_freq=1,
        callbacks = [cp_callback],
    )

    model.summary()      

def main():
    train_data = dataProcess()
    train(train_data)

if __name__ == '__main__':
    main()
    














