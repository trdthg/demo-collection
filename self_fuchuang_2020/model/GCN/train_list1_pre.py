from PIL import Image
import numpy as np
import pandas as pd
import pymysql
import tensorflow as tf
from tensorflow.keras.layers import Dense, GRU, Dropout, GRU, LSTM, Embedding
import datetime

try:
    from GCN.DB import DB
except:
    from DB import DB

m = 14 * 29
n = 3 * 29


def getAllData():
    data = pd.read_csv('./data/list1_flow.csv', header=None).values
    aaa = []
    for i in range(len(data)-m):
        aaa.append(data[i:i+m])
    return np.array(aaa)

def getNearestData():
    data = pd.read_csv('./data/list1_flow.csv', header=None).values
    aaa = []
    aaa.append(data[-m:])
    return np.array(aaa)

def load_model():
    checkpoint_save_path = "savedata/train_list1_31.ckpt"
    model = tf.keras.Sequential([
        GRU(256, return_sequences=True),
        GRU(512),
        Dropout(0.1),
        Dense(1024, activation='swish'),
        Dense(4096, activation='swish'),
        Dense(162*4*n),
    ])

    model.load_weights(checkpoint_save_path).expect_partial()

    return model

def predict(model):
    

    time_start_list = []
    for month in (3,4,5,6):
        for day in range(1, 30):
            for hour in range(6, 23):
                for minute in [0, 30]:
                    time_start_list.append(f'{month}-{day}:{hour}:{minute}')
    time_start_list = time_start_list[14:]
    print('len: ',len(time_start_list))
    aaa = getAllData()
    print(aaa.shape)
    # for i in aaa:
    data_for_db = {month:[] for month in [1,2,3,4,5,6,7,8,9,10,11,12]}
    station_order = [65.0, 49.0, 149.0, 74.0, 128.0, 34.0, 106.0, 110.0, 97.0, 80.0, 89.0, 64.0, 150.0, 154.0, 107.0, 83.0, 108.0, 47.0, 159.0, 1.0, 63.0, 129.0, 9.0, 163.0, 53.0, 79.0, 18.0, 123.0, 127.0, 81.0, 27.0, 48.0, 151.0, 68.0, 52.0, 76.0, 57.0, 71.0, 139.0, 105.0, 51.0, 24.0, 143.0, 156.0, 61.0, 50.0, 119.0, 66.0, 12.0, 161.0, 21.0, 133.0, 22.0, 138.0, 41.0, 30.0, 67.0, 144.0, 29.0, 126.0, 115.0, 40.0, 131.0, 39.0, 100.0, 135.0, 167.0, 113.0, 141.0, 142.0, 158.0, 44.0, 117.0, 147.0, 42.0, 35.0, 87.0, 109.0, 33.0, 112.0, 153.0, 125.0, 121.0, 11.0, 157.0, 114.0, 168.0, 134.0, 85.0, 2.0, 4.0, 103.0, 145.0, 88.0, 94.0, 160.0, 7.0, 6.0, 8.0, 75.0, 102.0, 90.0, 84.0, 59.0, 19.0, 62.0, 165.0, 38.0, 58.0, 43.0, 10.0, 96.0, 132.0, 37.0, 16.0, 69.0, 54.0, 56.0, 45.0, 152.0, 164.0, 82.0, 111.0, 140.0, 13.0, 70.0, 55.0, 20.0, 23.0, 118.0, 162.0, 15.0, 86.0, 46.0, 3.0, 25.0, 146.0, 130.0, 120.0, 77.0, 122.0, 36.0, 28.0, 124.0, 166.0, 99.0, 136.0, 137.0, 101.0, 31.0, 17.0, 26.0, 95.0, 72.0, 93.0, 92.0, 116.0, 32.0, 91.0, 60.0, 148.0, 73.0]
    result = model.predict(aaa)
    print(result.shape)
    for i, flows in enumerate(result):
        for j, flow in enumerate(flows):
            if j%4 != 0:
                continue
            station = f'Sta{int(station_order[j%162])}'
            in_flow = flows[j]
            out_flow = flows[j+1]
            in_flow_plus = flows[j+2]
            out_flow_plus = flows[j+3]
            which_turn = i%n + 1
            time_start = time_start_list[i]
            data_for_db[int(time_start.split("-")[0])].append([str(station), float(in_flow), float(out_flow), float(in_flow_plus), float(out_flow_plus), str(time_start.split("-")[1]), int(which_turn)])
    return data_for_db
    print('---------------over------------------')

def predict_web(model, info, a = True):
    print('-----list1-----')
    station_order = [65.0, 49.0, 149.0, 74.0, 128.0, 34.0, 106.0, 110.0, 97.0, 80.0, 89.0, 64.0, 150.0, 154.0, 107.0, 83.0, 108.0, 47.0, 159.0, 1.0, 63.0, 129.0, 9.0, 163.0, 53.0, 79.0, 18.0, 123.0, 127.0, 81.0, 27.0, 48.0, 151.0, 68.0, 52.0, 76.0, 57.0, 71.0, 139.0, 105.0, 51.0, 24.0, 143.0, 156.0, 61.0, 50.0, 119.0, 66.0, 12.0, 161.0, 21.0, 133.0, 22.0, 138.0, 41.0, 30.0, 67.0, 144.0, 29.0, 126.0, 115.0, 40.0, 131.0, 39.0, 100.0, 135.0, 167.0, 113.0, 141.0, 142.0, 158.0, 44.0, 117.0, 147.0, 42.0, 35.0, 87.0, 109.0, 33.0, 112.0, 153.0, 125.0, 121.0, 11.0, 157.0, 114.0, 168.0, 134.0, 85.0, 2.0, 4.0, 103.0, 145.0, 88.0, 94.0, 160.0, 7.0, 6.0, 8.0, 75.0, 102.0, 90.0, 84.0, 59.0, 19.0, 62.0, 165.0, 38.0, 58.0, 43.0, 10.0, 96.0, 132.0, 37.0, 16.0, 69.0, 54.0, 56.0, 45.0, 152.0, 164.0, 82.0, 111.0, 140.0, 13.0, 70.0, 55.0, 20.0, 23.0, 118.0, 162.0, 15.0, 86.0, 46.0, 3.0, 25.0, 146.0, 130.0, 120.0, 77.0, 122.0, 36.0, 28.0, 124.0, 166.0, 99.0, 136.0, 137.0, 101.0, 31.0, 17.0, 26.0, 95.0, 72.0, 93.0, 92.0, 116.0, 32.0, 91.0, 60.0, 148.0, 73.0]
    workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
    workday['date'] = pd.to_datetime(workday['Column1'],format="%Y%m%d")
    aaa = getNearestData()
    # print(aaa.shape)
    ori_dict = {
        'time': 0,  
        'weather': None, 
        'dayprop': None, 
        'temperatures': None, 
        'station': {
            'name': 'Sta65',
            'flow': 0,
            'flow_type': 0, 
            'type': None, 
            'station_classify': None, 
        }
    }
    if info and a:
        for key in info.keys():
            if key == 'time':
                result = predict_web(model, info, False)
                result = result[0]
                # [det, int(seconds/60/30), a.date, b.date()] = info['time']
                # month, dayprop, anyday, hour, noon weather_kind temperatures station_labels_ int(info[1]) which_line flow
                ccc = []
                print(info[key][0])
                for i in range(info[key][0]):
                    if i <= info[key][1]:
                        month, day, hour = info[key][2].date().month, info[key][2].date().day, info[key][2].hour
                        dayprop = np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]
                    elif info[key][1] + 34:
                        month, day, hour = info[key][2].date().month, info[key][2].date().day, info[key][2].hour
                        dayprop = np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]
                    anyday=datetime.datetime(2020,month,day).strftime("%w");
                    if hour<=12:
                        noon = 0
                    else:
                        noon = 1
                    weather_kind = [0,0,0,0,0,0,0,0]
                    temperatures = [0, 0]
                    station_labels_ = [0,0,0,0,0]
                    transfor_station = [0]
                    which_line = [0,0,0,0,0,0,0,0]
                    flow = result[i*4*162:(i+1)*4*162]
                    k = station_labels_ + transfor_station + which_line
                    bbb = [month, dayprop, anyday, hour, noon]
                    bbb.extend(weather_kind)
                    bbb.extend(temperatures)
                    for i in range(162):
                        bbb.extend(k)
                        bbb.extend(flow[i*4:(i+1)*4])
                    ccc.append(bbb)
                ccc = np.array(ccc, dtype='float16')
                print(aaa.shape, ccc.shape)
                aaa[0] = np.r_[aaa[0][-(m-info[key][0]):], ccc]
                aaa[0] = aaa[0][:m]
                print(aaa)
            elif key == 'weather':
                aaa[0][:5:5+8] = info[key][0]
            elif key == 'temperatures':
                aaa[0][:,13:13+2] = info[key] 
            elif key == 'dayprop':
                aaa[0][:,1] = info[key]
            elif key == 'station':
                name = info[key]['name']
                head_index = 162*18-station_order.index(float(name[3:]))*18
                print(head_index, type(head_index))
                if 'flow' in info[key].keys():
                    # 一个站有11项数据
                    aaa[0][0,-head_index+14 + info[key]['flow'][1]] += info[key]['flow'][0]
                if 'type' in info[key].keys():
                    aaa[0][:,-head_index+5] = info[key]['type'] 
                if 'station_classify' in info[key].keys():
                    aaa[0][:,-head_index:-head_index+5] = info[key]['station_classify']
        
    result = model.predict(aaa)
    # print(result.shape)
    if a:
        result = np.round(result)
        result = result.astype(np.int16)
        data_for_web = []
        for i, flows in enumerate(result):
            for j, flow in enumerate(flows):
                if j%4 != 0:
                    continue
                station = f'Sta{int(station_order[j%162])}'
                in_flow = flows[j]
                out_flow = flows[j+1]
                in_flow_plus = flows[j+2]
                out_flow_plus = flows[j+3]
                which_turn = int(j/162/4) + 1
                data_for_web.append({'station':station, 'flow':[in_flow,out_flow,in_flow_plus,out_flow_plus], 'turn':which_turn})
        return data_for_web
    else:
        return result

def write_to_db(data):
    db = DB('library_flow')
    for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
        print(month)
        table_name_1 = f'list1_predict_{month}'
        db.cursor.executemany(f'INSERT INTO {table_name_1} VALUES(%s,%s,%s,%s,%s,%s,%s)', data[month])
        db.connect_info.commit()

def main():
    model = load_model()
    data = predict(model)
    # write_to_db(data)

if __name__ == '__main__':
    main()