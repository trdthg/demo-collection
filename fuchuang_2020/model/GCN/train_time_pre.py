
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Dense
import sklearn.preprocessing


def load_model():
    checkpoint_save_path = "savedata/train_time.ckpt"
    model = tf.keras.Sequential([
        Dense(2048, activation='swish'),
        Dense(256, activation='swish'),
        Dense(1)
    ])

    model.load_weights(checkpoint_save_path).expect_partial()

    return model

def predict(model, info):
    stationin = info['stationin']        
    stationout = info['stationout']        
    month = info['month']
    hour = info['hour']
    dayprop = info['dayprop']
    trips = pd.DataFrame(pd.read_csv('./data/trips.csv', encoding='gbk')).sort_values(by='进站时间').reset_index(drop=True)
    enc_sta = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
    enc_sta.fit_transform(np.array(trips['进站名称']).reshape(len(trips['进站名称']),1))
    stationin = enc_sta.transform([[stationin]])
    stationout = enc_sta.transform([[stationout]])
    a = list(stationin[0]) + list(stationout[0]) + [month, hour, dayprop]
    result = model.predict([a])
    result = np.round(result)
    return result[0][0]

def main():
    model = load_model()
    info = {
        'stationin': 'Sta24',
        'stationout': 'Sta45',
        'month': 5,
        'hour': 12,    
        'dayprop': 2,  
    }
    a = predict(model, info)
    print(a)

if __name__ == '__main__':
    main()