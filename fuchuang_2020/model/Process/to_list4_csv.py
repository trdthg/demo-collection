import os
import csv
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymysql
# import tensorflow as tf
# from tensorflow.keras.layers import Dense, GRU, Dropout, GRU, LSTM, Embedding
# from tensorflow.keras.utils import to_categorical
import sklearn.preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

print('正在处理输入数据')
# 1. 导入原始数据
year = 2020
station = pd.DataFrame(pd.read_csv('./data/station.csv', encoding='gbk'))
workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))

class DB():

    
    def __init__(self, library="library_flow"):
        super().__init__()
        self.connect(library)

    def connect(self,DB):
        DB_USER = 'maker0'
        DB_PASS = 'Maker0000'
        DB_HOST = 'rm-bp11labi01950io698o.mysql.rds.aliyuncs.com'
        DB_PORT = 3306
        DATABASE = DB
        try:
            self.connect_info = pymysql.connect(user=DB_USER, passwd=DB_PASS, host=DB_HOST, port=DB_PORT, db=DATABASE)  #1
            self.cursor = self.connect_info.cursor()
        except:
            print("连接失败")

class DataProcess():
    
    def __init__(self, db):
        super().__init__()
        self.cursor = db.cursor
        self.connect = db.connect

    def getOriData(self):
        # enc_weather = sklearn.preprocessing.OneHotEncoder(sparse=False) # Key here is sparse=False!
        # weather_kinds = ['多云', '中雨', '阴', '晴', '雷阵雨', '暴雨', '大雨', '小雨']
        # weather_onehot = enc_weather.fit_transform(np.array(weather_kinds).reshape(len(weather_kinds),1))
               
        weather = pd.DataFrame(pd.read_csv('./data/weather.csv', encoding='gbk'))
        workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
        workday['date'] = pd.to_datetime(workday['Column1'],format="%Y%m%d")
        year = 2020
        trainX = []
        # trainY = []
        weather_kinds = ['多云', '中雨', '阴', '晴', '雷阵雨', '暴雨', '大雨', '小雨']
        weather_kind = [0,0,0,0,0,0,0,0]
        for month in [3, 4, 5, 6]:
            for day in range(1, 30):
                # print(day)
                # 是否放假
                dayprop = np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]
                # 获取每天天气情况
                date = f'2020年{month}月{day}日'
                now_weather = ((weather.loc[weather['日期']==date]).values.tolist())[0]
                print(now_weather)
                weather_conditions = now_weather[1].split(' /')
                temperatures = (float((now_weather[2].split('℃'))[0]), float((now_weather[3].split('℃'))[0]))
                for hour in range(6, 23):
                    if hour<=12:
                        weather_condition = weather_conditions[0]
                        weather_kind[weather_kinds.index(weather_condition)] = 1
                        noon = 0
                    else:
                        weather_condition = weather_conditions[1]
                        weather_kind[weather_kinds.index(weather_condition)] = 1
                        noon = 1
                    for minute in range(0, 2):
                        time_start = f'{day}:{hour}:{30*minute}'
                        sql = f'SELECT linename, flow FROM list4_{month} WHERE time_start="{time_start}"'
                        ori_flow = self.cursor.execute(sql)
                        ori_flow = self.cursor.fetchall()
                        train = [month, dayprop, hour, noon]
                        train.extend(weather_kind)
                        train.extend(temperatures)
                        line_flow_dict = {}
                        for row in ori_flow:
                            line_flow_dict[row[0]] = row[1]
                        # trainy = []
                        for line_name in ['1号线', '2号线', '3号线', '4号线', '5号线', '10号线', '11号线', '12号线']:
                            flow = line_flow_dict.get(line_name, 0.)
                            train.append(flow)
                            # trainy.append(flow)
                        # print(train)
                        trainX.append(train)
                        # trainY.append(trainy)
        with open('./data/list4_flow.csv','w',newline='') as f:
            f = csv.writer(f)
            f.writerows(trainX)
        # with open('./list4_flow_trainY.csv','w',newline='') as f:
        #     f = csv.writer(f)
        #     f.writerows(trainY)






def main():
    
    db = DB()
    dp = DataProcess(db)
    dp.getOriData()


if __name__ == '__main__':
    main()
