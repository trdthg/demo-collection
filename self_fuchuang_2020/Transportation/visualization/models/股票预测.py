import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, SimpleRNN, Dropout
import matplotlib.pyplot as plt
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math
import datetime
import sklearn


# summary_writer = tf.summary.create_file_writer('./tensorboard')     # 参数为记录文件所保存的目录


df = pd.DataFrame(pd.read_csv('./sta_flow_by_day.csv'))
motai = df.loc[df['sta']=='Sta65']

train_set = motai.iloc[:,3:4].values
test_set = motai.iloc[:,3:4].values


# !! 归一化 !!
sc = MinMaxScaler(feature_range=(0,1))
print(train_set)
train_set_scaled = sc.fit_transform(train_set)
test_set = sc.transform(test_set)
x_train = []
y_train = []
x_test = []
y_test = []

for i in range(10, len(train_set_scaled)):
    print(train_set_scaled[i-10:i, 0])
    print(train_set_scaled[i-10:i, 0].shape)
    x_train.append(train_set_scaled[i-10:i, 0])
    y_train.append(train_set_scaled[i, 0])
np.random.seed(7)
np.random.shuffle(x_train)
np.random.seed(7)
np.random.shuffle(y_train)
tf.random.set_seed(7)
print('-'*50)
x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0], 10 , 1))
fish = '🐟'
for i in range(10, len(test_set)):
    x_test.append(test_set[i-10:i, 0])
    y_test.append(test_set[i,0])

x_test, y_test = np.array(x_test), np.array(y_test)
x_test = np.reshape(x_test, (x_test.shape[0], 10, 1))

print(x_train[0])
model = tf.keras.Sequential([
    SimpleRNN(20, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
    SimpleRNN(25, return_sequences=True),  # 两层都是RNN时,前一层要加上return_sequences=True
    Dropout(0.2),  # 随即扔掉一些神经元, 防止过拟合, 可以先设为0, 逐渐调大, 找到最优值
    SimpleRNN(20),
    Dropout(0.1),
    Dense(1),
])

model.compile(
    optimizer = tf.keras.optimizers.Adam(0.00001),
    loss = tf.keras.losses.mean_squared_error,
)

# checkpoint_save_path = './savedata/stock1.ckpt'
# if os.path.exists(checkpoint_save_path + '.index'):
#     print('-----------------load the model------------------')
#     model.load_weights(checkpoint_save_path)

# cp_callback = tf.keras.callbacks.ModelCheckpoint(
#     filepath = checkpoint_save_path,
#     save_weights_only = True,
#     save_best_only = True,
#     # monitor = 'var_loss', # 指定需要监测的值
# )

# log_dir="logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

history = model.fit(
    x_train, y_train,
    batch_size=1, epochs=100,
    validation_split=0.2,

    # validation_data=(x_test, y_test),
    validation_freq=1,
    # callbacks = [cp_callback,tensorboard_callback],
)

model.summary()

print(np.array(x_test).shape)
predicted_stock_price = model.predict(x_test)
print(predicted_stock_price.shape)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)
real_stock_price = sc.inverse_transform(test_set[10:])

plt.plot(real_stock_price, c='r', label='Real Price')
plt.plot(predicted_stock_price, c='b', label='Predict Price')
plt.legend()
loss = history.history['loss']
val_loss = history.history['val_loss']
plt.figure()
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()