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
print('正在处理输入数据')
# 1. 导入原始数据
year = 2020
station = pd.DataFrame(pd.read_csv('./data/station.csv', encoding='gbk'))
workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
df = pd.DataFrame(pd.read_csv('./csv/sta_flow_by_day.csv'))
df = df.loc[df['sta']=='Sta65']
# print(df)

# route. sta. dist. 星期几. 是否放假. 票价(不管). 

# # 2. 把route列转为onehot编码
# routes = []
# for sta in np.array(df['sta']):
#     route = np.array(station.loc[station['站点名称']==sta]['线路'])
#     # print(route)
#     routes.append(str(route))
# enc_route = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
# route_onehot = enc_route.fit_transform(np.array(routes).reshape(len(df['sta']),1))
# # print(len(route_onehot))

# # 3. 将sta转为onehot编码
# enc_sta = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
# sta_onehot = enc_sta.fit_transform(np.array(df['sta']).reshape(len(df['sta']),1))
# # print(sta_onehot)

# # 4. 将dist转为onehot编码
# dists = []
# for sta in np.array(df['sta']):
#     dist = np.array(station.loc[station['站点名称']==sta]['行政区域'])
#     dists.append(str(dist))
# enc_dist = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
# dist_onehot = enc_dist.fit_transform(np.array(dists).reshape(len(df['sta']),1))
# # print(sta_onehot)

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
# print(daily_flow_scaled.shape)

x_train_1, y_train_1 = [], []
x_train, y_train = [], []
x_test = []

for anyday, dayprop, dayprop_num, month, day, flow in zip( anydays, dayprop_onehot, dayprops, np.array(df['month']), np.array(df['day']), np.array(daily_flow_scaled)):
    # print(dayprop_num)
    # x_arr =  [flow[0], month , ]
    x_arr =  [ flow[0], ] + list(dayprop) + [month, int(anyday)]
    # x_arr =   [ flow[0]] + [int(anyday), month, day, ]
    y_arr = flow
    # print(y_arr)
    x_train_1.append(x_arr)
    y_train_1.append(y_arr)
    # print(x_arr)
    # print(y_arr)
    # break
    # print(len(x_arr))

print('-'*50)
# print(x_train)
# x_train_1, y_train_1 = pd.DataFrame(x_train_1), pd.DataFrame(y_train_1)
x_train_1 = pd.DataFrame(x_train_1).values
y_train_1 = pd.DataFrame(y_train_1).values


for i in range(14, len(x_train_1)):
    # print(np.array(x_train_1[i-14:i, :]).reshape(1,-1)[0])
    # print(x_train_1[i-14:i, :].shape)
    x_train.append(np.array(x_train_1[i-14:i, :]).reshape(1,-1)[0])
    x_test.append(np.array(x_train_1[i-14:i, :]).reshape(1,-1)[0])

    # print([x_train_1[i, 0]])
    y_train.append([x_train_1[i, 0]])
np.random.seed(7)
np.random.shuffle(x_train)
np.random.seed(7)
np.random.shuffle(y_train)
tf.random.set_seed(7)

x_train, y_train = np.array(x_train), np.array(y_train)
x_test = np.array(x_test)
print(x_train.shape)
x_train = np.reshape(x_train, (x_train.shape[0], 14, len(x_arr)))
x_test = np.reshape(x_test, (x_test.shape[0], 14, len(x_arr)))
print(x_train[0])
print(x_test[0])
print(y_train[0])

for i in range(i):
    print("正在搭建模型")
    model = tf.keras.Sequential([
        # Embedding(503, 64),
        # GRU(16, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
        # Dropout(0.2),  # 随即扔掉一些神经元, 防止过拟合, 可以先设为0, 逐渐调大, 找到最优值
        # GRU(128, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
        # Dropout(0.2),  # 随即扔掉一些神经元, 防止过拟合, 可以先设为0, 逐渐调大, 找到最优值
        # GRU(128, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
        # Dropout(0.2),  # 随即扔掉一些神经元, 防止过拟合, 可以先设为0, 逐渐调大, 找到最优值
        # GRU(64),  # 两层都是RNN时,前一层要加上return_sequences=True
        # Dropout(0.2),
        # GRU(150, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
        # Dropout(0.5),
        # GRU(100, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
        # Dropout(0.5),   
        # GRU(50, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
        # Dropout(0.2),
        # GRU(25, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
        # Dropout(0.2),
        # GRU(160, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
        # Dropout(0.2),
        # GRU(160, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
        # Dropout(0.2),
        # GRU(180, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
        # Dropout(0.2),  # 随即扔掉一些神经元, 防止过拟合, 可以先设为0, 逐渐调大, 找到最优值
        # GRU(140, return_sequences=True),
        # Dropout(0.2),
        GRU(300),
        Dropout(0.5),
        Dense(1),
        # Dropout(0.2),
        # Dense(1),
        # tf.keras.layers.Flatten(),
        # GRU(3, return_sequences=True),
        # GRU(1),
        # tf.keras.layers.Dense(512, activation='swish'),
        # tf.keras.layers.Dense(512, activation='swish'),
        # tf.keras.layers.Dense(256, activation='swish'),
        # tf.keras.layers.Dense(256, activation='swish'),
        # Dense(0.2),
        # Dense(0.2),
        # tf.keras.layers.Dense(128, activation='swish'),
        # tf.keras.layers.Dense(128, activation='swish'),
        # tf.keras.layers.Dense(64, activation='swish'),
        # tf.keras.layers.Dense(64, activation='swish'),
        # tf.keras.layers.Dense(32, activation='swish'),
        # tf.keras.layers.Dense(32, activation='swish'),
        # tf.keras.layers.Dense(16, activation='swish'),
        # tf.keras.layers.Dense(16, activation='swish'),
        # tf.keras.layers.Dense(8, activation='swish'),
        # tf.keras.layers.Dense(8, activation='swish'),
        # Dense(1)
        # tf.keras.layers.Dense(64, activation='swish',kernel_regularizer=tf.keras.regularizers.l2()),
    ])

    model.compile(
        optimizer = tf.keras.optimizers.Adam(0.0001),
        # optimizer = tf.keras.optimizers.Adadelta(),
        loss = tf.keras.losses.mean_squared_error,
        # loss = tf.keras.losses.categorical_crossentropy,
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
    print("开始训练")
    history = model.fit(
        x_train, y_train,
        batch_size=1, epochs=50,
        validation_split=0.2,
        validation_freq=1,
        # callbacks = [cp_callback],
    )

    model.summary()      


    predict_ori = model.predict(x_test)
    print(predict_ori.shape)


    predict = sc.inverse_transform(predict_ori)
    print(predict.shape)
    print("开始做图")

    df = pd.DataFrame(pd.read_csv('.csv/sta_flow_by_day.csv'))
    i=0
    plt.figure()
    for sta in np.array(station.loc[station['线路']=='1号线']['站点名称']):
        i+=1
        # plt.figure()
        if sta=='Sta65':
            print(sta)
            df_ = df.loc[(df['sta'] == sta)]
            # x = range(0, len(np.array(df_['month'])))[15:]
            X = [str(f'{month}.{day}') for month, day in zip(np.array(df_['month']), np.array(df_['day']))][14:]
            Y = np.array(df_['flow'])[14:]
            plt.plot( X,Y, label=sta)
            plt.xticks(range(len(X)), X, rotation=270)
            plt.legend()
            break
    # plt.figure()
    plt.plot(X, predict, c='r', label='Predict')
    # plt.xticks(range(len(X)), X, rotation=270)
    plt.legend()


    loss = history.history['loss']
    val_loss = history.history['val_loss']
    plt.figure()
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.show()


















