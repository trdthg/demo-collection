import os
import csv
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Dense, GRU, Dropout, GRU, LSTM, Embedding
import sklearn.preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.utils import to_categorical
print('正在处理输入数据')

# 1 导入数据集
traindata = pd.read_csv('./data/list4_flow.csv', header=None, dtype='float32').values
_trainX = traindata
_trainY = traindata[:, -8:]
trainX, trainY = [], []
m = 14 * 29
n = 3 * 29
for i in range(len(_trainX)-m-n):
    trainX.append(_trainX[i:i+m])
    # trainY.append(_trainY[i+14:i+15])
    trainY.append(_trainY[i+m:i+m+n].flatten())
trainX, trainY = np.array(trainX), np.array(trainY)
np.random.seed(7)
np.random.shuffle(trainX)
np.random.seed(7)
np.random.shuffle(trainY)
tf.random.set_seed(7)

#
model = tf.keras.Sequential([
    # GRU(256, return_sequences=True),
    GRU(256),
    # Dropout(0.1),
    Dense(512, activation='swish'),
    Dense(n*8)
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(0.0001),
    # loss=tf.keras.losses.categorical_crossentropy,
    loss=tf.keras.losses.mean_squared_error,
)

checkpoint_save_path = "savedata/train_list4_29.ckpt"

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

predict = model.predict(trainX[-200:])
predict = [item[2] for item in predict]
train = [item[2] for item in trainY[-200:]]
print(len(predict))
print(len(train))
plt.figure()
plt.plot(predict, label='predict')
plt.plot(train, label='train')
plt.legend()

loss = history.history['loss']
val_loss = history.history['val_loss']
plt.figure()
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()