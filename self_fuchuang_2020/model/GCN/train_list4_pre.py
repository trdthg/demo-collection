from PIL import Image
import numpy as np
import pandas as pd
import pymysql
import tensorflow as tf
from tensorflow.keras.layers import Dense, GRU, Dropout, GRU, LSTM, Embedding

try:
    from GCN.DB import DB
except:
    from DB import DB
    
stationinfo_dict = {'Sta1': ['1号线', '0'],'Sta159': ['1号线', '0'],'Sta108': ['1号线', '0'],'Sta83': ['1号线', '0'],'Sta107': ['1号线', '0'],'Sta154': ['1号线', '0'],'Sta150': ['1号线', '0'],'Sta64': ['1号线', '0'],'Sta89': ['1号线', '1'],'Sta80': ['1号线', '0'],'Sta97': ['1号线', '0'],'Sta110': ['1号线', '0'],'Sta106': ['1号线', '0'],'Sta34': ['1号线', '0'],'Sta128': ['1号线', '0'],'Sta74': ['1号线', '0'],'Sta149': ['1号线', '0'],'Sta49': ['1号线', '0'],'Sta65': ['1号线', '0'],'Sta9': ['2号线', '0'],'Sta163': ['2号线', '0'],'Sta53': ['2号线', '0'],'Sta78': ['2号线', '0'],'Sta79': ['2号线', '0'],'Sta18': ['2号线', '0'],'Sta123': ['2号线', '0'],'Sta127': ['2号线', '1'],'Sta81': ['2号线', '0'],'Sta27': ['2号线', '0'],'Sta48': ['2号线', '0'],'Sta151': ['2号线', '0'],'Sta68': ['2号线', '0'],'Sta52': ['2号线', '0'],'Sta76': ['2号线', '0'],'Sta57': ['2号线', '0'],'Sta71': ['2号线', '0'],'Sta139': ['2号线', '0'],'Sta24': ['2号线', '0'],'Sta105': ['2号线', '0'],'Sta51': ['2号线', '0'],'Sta143': ['3号线', '0'],'Sta156': ['3号线', '0'],'Sta61': ['3号线', '0'],'Sta50': ['3号线', '0'],'Sta119': ['3号线', '0'],'Sta66': ['3号线', '0'],'Sta12': ['3号线', '0'],'Sta161': ['3号线', '0'],'Sta21': ['3号线', '0'],'Sta133': ['3号线', '0'],'Sta22': ['3号线', '0'],'Sta138': ['3号线', '0'],'Sta41': ['3号线', '1'],'Sta30': ['3号线', '0'],'Sta67': ['3号线', '0'],'Sta144': ['3号线', '0'],'Sta29': ['3号线', '0'],'Sta126': ['3号线', '0'],'Sta40': ['3号线', '0'],'Sta131': ['3号线', '0'],'Sta39': ['3号线', '0'],'Sta100': ['3号线', '0'],'Sta167': ['3号线', '0'],'Sta113': ['3号线', '0'],'Sta141': ['3号线', '0'],'Sta142': ['3号线', '0'],'Sta158': ['3号线', '0'],'Sta44': ['3号线', '0'],'Sta117': ['3号线', '0'],'Sta147': ['3号线', '0'],'Sta42': ['3号线', '0'],'Sta35': ['3号线', '0'],'Sta109': ['3号线', '0'],'Sta33': ['3号线', '0'],'Sta112': ['3号线', '0'],'Sta153': ['3号线', '0'],'Sta125': ['3号线', '0'],'Sta121': ['3号线', '0'],'Sta11': ['3号线', '0'],'Sta134': ['10号线', '1'],'Sta59': ['4号线', '0'],'Sta19': ['4号线', '0'],'Sta62': ['4号线', '0'],'Sta165': ['4号线', '0'],'Sta58': ['4号线', '0'],'Sta38': ['4号线', '0'],'Sta43': ['5号线', '0'],'Sta10': ['5号线', '0'],'Sta96': ['5号线', '0'],'Sta132': ['5号 线', '0'],'Sta37': ['5号线', '0'],'Sta16': ['5号线', '0'],'Sta69': ['5号线', '0'],'Sta54': ['5号线', '0'],'Sta120': ['11号线', '0'],'Sta130': ['11号线', '0'],'Sta146': ['11号线', '0'],'Sta25': ['11号线', '0'],'Sta3': ['11号线', '1'],'Sta46': ['11号线', '0'],'Sta86': ['11号线', '0'],'Sta15': ['11号线', '1'],'Sta162': ['11号线', '0'],'Sta118': ['11号线', '0'],'Sta20': ['11号线', '0'],'Sta55': ['11号线', '0'],'Sta70': ['11号线', '0'],'Sta13': ['11号线', '0'],'Sta140': ['11号线', '1'],'Sta77': ['11号线', '0'],'Sta122': ['11号线', '0'],'Sta36': ['11号线', '0'],'Sta166': ['11号线', '0'],'Sta99': ['11号线', '0'],'Sta124': ['11号线', '0'],'Sta28': ['11号线', '0'],'Sta82': ['11号线', '0'],'Sta164': ['11号线', '0'],'Sta152': ['11号线', '0'],'Sta45': ['11号线', '0'],'Sta75': ['10号线', '1'],'Sta136': ['12号线', '0'],'Sta137': ['12号线', '0'],'Sta101': ['12号线', '0'],'Sta17': ['12号线', '0'],'Sta26': ['12号线', '0'],'Sta90': ['12号线', '1'],'Sta95': ['12号线', '0'],'Sta93': ['12号线', '0'],'Sta92': ['12号线', '0'],'Sta32': ['12号线', '0'],'Sta91': ['12号线', '0'],'Sta157': ['10号线', '0'],'Sta168': ['10号线', '0'],'Sta85': ['10号线', '0'],'Sta2': ['10号线', '0'],'Sta4': ['10号线', '0'],'Sta103': ['10号线', '0'],'Sta145': ['10号线', '0'],'Sta88': ['10号线', '0'],'Sta94': ['10号线', '0'],'Sta160': ['10号线', '0'],'Sta7': ['10号线', '0'],'Sta6': ['10号线', '0'],'Sta8': ['10号线', '0'],'Sta102': ['10号线', '0'],'Sta31': ['12号线', '0'],'Sta72': ['12号线', '0'],'Sta116': ['12号线', '0'],'Sta129': ['2号线', '0'],'Sta47': ['2号线', '1'],'Sta60': ['12号线', '0'],'Sta148': ['12号线', '0'],'Sta73': ['12号线', '0'],'Sta23': ['11号线', '1'],'Sta56': ['11号线', '1'],'Sta115': ['11号线', '1'],'Sta63': ['11号线', '1'],'Sta114': ['10号线', '1'],'Sta135': ['10号线', '1'],'Sta87': ['10号线', '1'],'Sta84': ['4号线', '0'],'Sta111': ['11号线', '0']}
station_order = ['1号线', '2号线', '3号线', '4号线', '5号线', '10号线', '11号线', '12号线']

m = 14 * 29
n = 3 * 29

def getAllData():
    data = pd.read_csv('./data/list4_flow.csv', header=None).values
    aaa = []
    for i in range(len(data)-m):
        aaa.append(data[i:i+m])
    return np.array(aaa)

def getNearestData():
    data = pd.read_csv('./data/list4_flow.csv', header=None).values
    aaa = []
    aaa.append(data[-m:])
    return np.array(aaa)

def load_model():
    checkpoint_save_path = "savedata/train_list4_29.ckpt"

    model = tf.keras.Sequential([
        # GRU(256, return_sequences=True),
        GRU(256),
        # Dropout(0.1),
        Dense(512, activation='swish'),
        Dense(8*n)
    ])

    model.load_weights(checkpoint_save_path).expect_partial()
    return model


def predict_web(model, info, a = True):
    print('-----list4-----')
    # if info['time']
    # month, dayprop, anyday, hour, noon, weather_kind, temperatures, 是否换成, 几号线,
    # ori_dict = {
    #     'time': 0,  
    #     'weather': None, 
    #     'dayprop': None, 
    #     'temperatures': None, 
    #     'station': {
    #         'name': 'Sta65',
    #         'flow': 0,
    #         'flow_type': 0, 
    #         'type': None, 
    #         'station_classify': None, 
    #     }
    # }        

    aaa = getNearestData()
    print(aaa.shape)
    if info and a:
        workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
        workday['date'] = pd.to_datetime(workday['Column1'],format="%Y%m%d")
        for key in info.keys():
            if key == 'time':
                # 直接先无脑预测一波
                result = predict_web(model, info, False)
                result = result[0]
                # [det, int(seconds/60/30), a.date, b.date()] = info['time']
                ccc = []
                print(info[key][0])
                for i in range(info[key][0]):
                    if i <= info[key][1]:
                        month, day, hour = info[key][2].date().month, info[key][2].date().day, info[key][2].hour
                        dayprop = np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]
                    elif info[key][1] + 34:
                        month, day, hour = info[key][2].date().month, info[key][2].date().day, info[key][2].hour
                        dayprop = np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]

                    if hour<=12:
                        noon = 0
                    else:
                        noon = 1
                    weather_kind = [0,0,0,0,0,0,0,0]
                    temperatures = [0, 0]
                    flow = result[i*8:(i+1)*8]
                    
                    bbb = [month, dayprop, hour, noon]
                    bbb.extend(weather_kind)
                    bbb.extend(temperatures)
                    bbb.extend(flow)
                    ccc.append(bbb)
                ccc = np.array(ccc, dtype='float16')
                print(aaa.shape, ccc.shape)
                aaa[0] = np.r_[aaa[0][-(m-info[key][0]):], ccc]
                aaa[0] = aaa[0][:m]
                print(aaa)
                # month, dayprop, hour, noon weather_kind temperatures flow
                # 之后再改数据
            elif key == 'weather':
                aaa[0][:4:4+8] = info[key][0]
            elif key == 'temperatures':
                aaa[0][:,12:12+2] = info[key]
            elif key == 'dayprop':
                aaa[0][:,1] = info[key]
            elif key == 'station':
                if 'flow' in info[key]['flow']: 
                    aaa[0][0,-(8-station_order.index(stationinfo_dict[info[key]][0]))] += info[key]['flow'][0]
            
    # for i in aaa:
    result = model.predict(aaa)
    if a:
        result = np.round(result)
        result = result.astype(np.int16)
        data_for_web = []
        print(result.shape)
        n = 3
        for i, flows in enumerate(result):
            for j, flow in enumerate(flows):
                station = station_order[j%8]
                flow = flows[j]
                which_turn = int(j/8) + 1
                # print(which_turn)
                data_for_web.append({'line':station, 'flow':flow, 'turn':which_turn})

        return data_for_web
    else:
        return result


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
    station_order = ['1号线', '2号线', '3号线', '4号线', '5号线', '10号线', '11号线', '12号线']
    result = model.predict(aaa)

    print(result.shape)
    n = 3
    for i, flows in enumerate(result):
        for j, flow in enumerate(flows):
            station = station_order[j%8]
            flow = flows[j]
            which_turn = i%n + 1
            time_start = time_start_list[i]
            data_for_db[int(time_start.split("-")[0])].append([station, float(flow), time_start.split("-")[1], int(which_turn)])

    return data_for_db
    print('---------------over------------------')

def write_to_db(data):
    db = DB('library_flow')
    for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
        print(month)
        table_name_1 = f'list4_predict_{month}'
        db.cursor.executemany(f'INSERT INTO {table_name_1} VALUES(%s,%s,%s,%s)', data[month])
        db.connect_info.commit()

def main():
    data = predict()

    write_to_db(data)
if __name__ == '__main__':
    main()