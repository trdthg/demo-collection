import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, SimpleRNN, Dropout, GRU, LSTM
import matplotlib.pyplot as plt
import os
import pandas as pd
import sklearn.preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.utils import to_categorical
# 1. 导入原始数据
df = pd.DataFrame(pd.read_csv('./sta_flow_by_month.csv'))
print(df)

# 2. 把route列转为onehot编码
enc_route = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
route_onehot = enc_route.fit_transform(np.array(list(df['route'])).reshape(len(df['route']),1))
print(df['route'].shape)
print(route_onehot)

# 3. 将sta转为onehot编码
enc_sta = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
sta_onehot = enc_sta.fit_transform(np.array(df['sta']).reshape(len(df['sta']),1))
print(sta_onehot)


# 4. 将每月流量进行归一化处理
month_set = df.iloc[:, 2:15].values
sc = MinMaxScaler(feature_range=(0,1))
month_set_scaled = sc.fit_transform(month_set)
print(month_set_scaled)

x_train, y_train = [], []
for route, sta, month in zip(route_onehot, sta_onehot, month_set_scaled):
    x_arr = list(route) + list(sta)
    y_arr = month
    x_train.append(x_arr)
    y_train.append(y_arr)
# print(x_train)
np.random.shuffle(x_train)
np.random.shuffle(y_train)

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1]))
print(x_train.shape)


model = tf.keras.Sequential([
    # tf.keras.layers.Embedding(x_train.shape[1], 32),
    # tf.keras.layers.Flatten(),
    # GRU(3),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    # Dense(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    Dense(0.2),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    # tf.keras.layers.Dense(64, activation='relu',kernel_regularizer=tf.keras.regularizers.l2()),
    tf.keras.layers.Dense(12)
])

model.compile(
    optimizer = tf.keras.optimizers.Adam(0.0001),
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

history = model.fit(
    x_train, y_train,
    batch_size=32, epochs=1500,
    validation_split=0.2,
    validation_freq=1,
    # callbacks = [cp_callback],
)

model.summary()      

# 测试

route = ['1号线']
sta = ['Sta1']
print(np.array(route).shape)
route_onehot = enc_route.transform(np.array(route).reshape(len(route),1))
sta_onehot = enc_sta.transform(np.array(sta).reshape(len(sta),1))
x_test = []
for route, sta in zip(route_onehot, sta_onehot):
    x_arr = list(route) + list(sta)
    x_test.append(x_arr)
x_test = np.array(x_test)
predict = model.predict(x_test)
tf.print(predict)
predict = sc.inverse_transform(predict)
print(predict)


loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure()
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12], predict[0] ,c='r')
plt.plot([1,2,3,4,5,6,7,8,9,10,11,12], [896,45,381,861,1640,1358,334,0,0,0,0,40] ,c='b')

plt.figure()
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()

plt.show()























