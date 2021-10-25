# -*- coding: utf-8 -*-
import time
import csv
import datetime
from pyasn1.type.univ import Null

import pymysql
import numpy as np
import scipy.sparse as sp
import pandas as pd
import networkx as nx

import graph2
import dijkstra
# import station_classify

lr = 0.01
dropout = 0
verbose = 1
epochs = 30
weight_decay = 5e-4

stationinfo_dict = {'Sta1': ['1号线', '0'],'Sta159': ['1号线', '0'],'Sta108': ['1号线', '0'],'Sta83': ['1号线', '0'],'Sta107': ['1号线', '0'],'Sta154': ['1号线', '0'],'Sta150': ['1号线', '0'],'Sta64': ['1号线', '0'],'Sta89': ['1号线', '1'],'Sta80': ['1号线', '0'],'Sta97': ['1号线', '0'],'Sta110': ['1号线', '0'],'Sta106': ['1号线', '0'],'Sta34': ['1号线', '0'],'Sta128': ['1号线', '0'],'Sta74': ['1号线', '0'],'Sta149': ['1号线', '0'],'Sta49': ['1号线', '0'],'Sta65': ['1号线', '0'],'Sta9': ['2号线', '0'],'Sta163': ['2号线', '0'],'Sta53': ['2号线', '0'],'Sta78': ['2号线', '0'],'Sta79': ['2号线', '0'],'Sta18': ['2号线', '0'],'Sta123': ['2号线', '0'],'Sta127': ['2号线', '1'],'Sta81': ['2号线', '0'],'Sta27': ['2号线', '0'],'Sta48': ['2号线', '0'],'Sta151': ['2号线', '0'],'Sta68': ['2号线', '0'],'Sta52': ['2号线', '0'],'Sta76': ['2号线', '0'],'Sta57': ['2号线', '0'],'Sta71': ['2号线', '0'],'Sta139': ['2号线', '0'],'Sta24': ['2号线', '0'],'Sta105': ['2号线', '0'],'Sta51': ['2号线', '0'],'Sta143': ['3号线', '0'],'Sta156': ['3号线', '0'],'Sta61': ['3号线', '0'],'Sta50': ['3号线', '0'],'Sta119': ['3号线', '0'],'Sta66': ['3号线', '0'],'Sta12': ['3号线', '0'],'Sta161': ['3号线', '0'],'Sta21': ['3号线', '0'],'Sta133': ['3号线', '0'],'Sta22': ['3号线', '0'],'Sta138': ['3号线', '0'],'Sta41': ['3号线', '1'],'Sta30': ['3号线', '0'],'Sta67': ['3号线', '0'],'Sta144': ['3号线', '0'],'Sta29': ['3号线', '0'],'Sta126': ['3号线', '0'],'Sta40': ['3号线', '0'],'Sta131': ['3号线', '0'],'Sta39': ['3号线', '0'],'Sta100': ['3号线', '0'],'Sta167': ['3号线', '0'],'Sta113': ['3号线', '0'],'Sta141': ['3号线', '0'],'Sta142': ['3号线', '0'],'Sta158': ['3号线', '0'],'Sta44': ['3号线', '0'],'Sta117': ['3号线', '0'],'Sta147': ['3号线', '0'],'Sta42': ['3号线', '0'],'Sta35': ['3号线', '0'],'Sta109': ['3号线', '0'],'Sta33': ['3号线', '0'],'Sta112': ['3号线', '0'],'Sta153': ['3号线', '0'],'Sta125': ['3号线', '0'],'Sta121': ['3号线', '0'],'Sta11': ['3号线', '0'],'Sta134': ['10号线', '1'],'Sta59': ['4号线', '0'],'Sta19': ['4号线', '0'],'Sta62': ['4号线', '0'],'Sta165': ['4号线', '0'],'Sta58': ['4号线', '0'],'Sta38': ['4号线', '0'],'Sta43': ['5号线', '0'],'Sta10': ['5号线', '0'],'Sta96': ['5号线', '0'],'Sta132': ['5号线', '0'],'Sta37': ['5号线', '0'],'Sta16': ['5号线', '0'],'Sta69': ['5号线', '0'],'Sta54': ['5号线', '0'],'Sta120': ['11号线', '0'],'Sta130': ['11号线', '0'],'Sta146': ['11号线', '0'],'Sta25': ['11号线', '0'],'Sta3': ['11号线', '1'],'Sta46': ['11号线', '0'],'Sta86': ['11号线', '0'],'Sta15': ['11号线', '1'],'Sta162': ['11号线', '0'],'Sta118': ['11号线', '0'],'Sta20': ['11号线', '0'],'Sta55': ['11号线', '0'],'Sta70': ['11号线', '0'],'Sta13': ['11号线', '0'],'Sta140': ['11号线', '1'],'Sta77': ['11号线', '0'],'Sta122': ['11号线', '0'],'Sta36': ['11号线', '0'],'Sta166': ['11号线', '0'],'Sta99': ['11号线', '0'],'Sta124': ['11号线', '0'],'Sta28': ['11号线', '0'],'Sta82': ['11号线', '0'],'Sta164': ['11号线', '0'],'Sta152': ['11号线', '0'],'Sta45': ['11号线', '0'],'Sta75': ['10号线', '1'],'Sta136': ['12号线', '0'],'Sta137': ['12号线', '0'],'Sta101': ['12号线', '0'],'Sta17': ['12号线', '0'],'Sta26': ['12号线', '0'],'Sta90': ['12号线', '1'],'Sta95': ['12号线', '0'],'Sta93': ['12号线', '0'],'Sta92': ['12号线', '0'],'Sta32': ['12号线', '0'],'Sta91': ['12号线', '0'],'Sta157': ['10号线', '0'],'Sta168': ['10号线', '0'],'Sta85': ['10号线', '0'],'Sta2': ['10号线', '0'],'Sta4': ['10号线', '0'],'Sta103': ['10号线', '0'],'Sta145': ['10号线', '0'],'Sta88': ['10号线', '0'],'Sta94': ['10号线', '0'],'Sta160': ['10号线', '0'],'Sta7': ['10号线', '0'],'Sta6': ['10号线', '0'],'Sta8': ['10号线', '0'],'Sta102': ['10号线', '0'],'Sta31': ['12号线', '0'],'Sta72': ['12号线', '0'],'Sta116': ['12号线', '0'],'Sta129': ['2号线', '0'],'Sta47': ['2号线', '1'],'Sta60': ['12号线', '0'],'Sta148': ['12号线', '0'],'Sta73': ['12号线', '0'],'Sta23': ['11号线', '1'],'Sta56': ['11号线', '1'],'Sta115': ['11号线', '1'],'Sta63': ['11号线', '1'],'Sta114': ['10号线', '1'],'Sta135': ['10号线', '1'],'Sta87': ['10号线', '1'],'Sta84': ['4号线', '0'],'Sta111': ['11号线', '0']}
line_names_dict = {'1号线': 0,'2号线': 1,'3号线': 2,'4号线': 3,'5号线': 4,'10号线': 5,'11号线': 6,'12号线': 7,}
class PreProcess():

    def __init__(self, library="library_flow"):
        super().__init__()
        print('-'*100)
        self.dbconnect(library)
        reader = dijkstra.ReadFile()
        self.all_stations = reader.readTxt()

    def dbconnect(self,DB):
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

    def getGraph(self):
        # 1. 得到 A (所有节点的邻接矩阵)
        graph_dict = {}
        for this_line in self.all_stations:
            for station in this_line:
                graph_dict[float(station.getName()[3:])] = []
                result = station.getNearStations(station)
                for near_station in result:
                    if near_station != Null:
                        graph_dict[float(station.getName()[3:])].append(float(near_station.getName()[3:]))
        self.graph_dict = graph_dict
        print(graph_dict.keys())
        G=nx.Graph(graph_dict)
        # print(G.nodes.data())
        G_mat = nx.adjacency_matrix(G)
        print(type(G_mat))
        print(G_mat.toarray())
        # with open('G.csv','w',newline='') as f3:
        #     f3_csv = csv.writer(f3)
        #     f3_csv.writerows(G_mat.toarray())
        print('G.shape', G_mat.shape)
        # nx.draw(G,with_labels=True,node_size=50,node_color='r',width=0.1,edge_color='r',font_color=None,font_size=6)
        # plt.show()
        return G

    def getFlow(self, time_len=12, test_len=4):
        workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
        workday['date'] = pd.to_datetime(workday['Column1'],format="%Y%m%d")
        weather = pd.DataFrame(pd.read_csv('./data/weather.csv', encoding='gbk'))
        # station_labels = station_classify.main()
        station_labels = [3, 1, 3, 1, 0, 3, 0, 3, 0, 3, 2, 3, 0, 3, 4, 3, 4, 4, 3, 3, 2, 4, 3, 0, 0, 0, 0, 3, 1, 1, 3, 3, 3, 3,0, 3, 0, 0, 0, 0, 0, 0, 3, 3, 1, 0, 0, 0, 3, 0, 0, 0, 3, 3, 1, 4, 4, 3, 3, 2, 4, 4, 3, 0, 1, 3, 3, 0, 1, 1, 3, 3, 3, 0, 0, 3, 3, 0, 1, 1, 1, 0, 0, 0, 0, 3, 0, 0, 1, 3, 2, 1, 4, 1, 3, 3, 3, 0, 1, 1, 3, 3, 0, 1, 0, 3, 0, 0, 3, 3, 3, 0, 3, 1, 0, 3, 3, 0, 3, 0, 3, 0, 0, 3, 0]
        station_labels.extend([0 for i in range(100)])
        weather_kinds = ['多云', '中雨', '阴', '晴', '雷阵雨', '暴雨', '大雨', '小雨']
        # 2. 得到 X (特征矩阵)

        # x_train为进站流量信息, y_train包含了[进站流量, 线路流量, 断面流量]
        # 故一个batch要以一个时段的进站流量为单位
        x_train, y_train = [], []
        x_test, y_test = [], []
        for month in (3,4,5,6):
            print(month)
            for day in range(1, 30):
                # 得到星期几
                anyday=datetime.datetime(2020,month,day).strftime("%w");
                # 得到是否是节假日
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
                        weather_kind = [0,0,0,0,0,0,0,0]
                        weather_kind[weather_kinds.index(weather_condition)] = 1
                        noon = 0
                    else:
                        weather_condition = weather_conditions[1]
                        weather_kind[weather_kinds.index(weather_condition)] = 1
                        noon = 1
                    for minute in range(0, 2):
                        x_train_part, y_train_part = [], []
                        x_test_part, y_test_part = [], []
                        x_train_part = [month, dayprop, anyday, hour, noon]
                        x_train_part.extend(weather_kind)
                        x_train_part.extend(temperatures)
                        time_start = f'{day}:{hour}:{30*minute}'
                        sql = f'SELECT station, in_flow, out_flow, in_flow_plus, out_flow_plus FROM list1_{month} WHERE time_start = "{time_start}"'
                        self.cursor.execute(sql)
                        # 获取某一时段的流量原始数据
                        a = self.cursor.fetchall()
                        already_in_stations = []
                        staflow = []
                        x_train_dict, y_train_dict = {}, {}
                        for row in a:
                            already_in_stations.append(row[0])
                            x_train_dict[int(row[0][3:])] = [row[1], row[2], row[3], row[4]]
                            # y_train_dict[float(row[0][3:])] = row[2]
                        for i, key in enumerate([65.0, 49.0, 149.0, 74.0, 128.0, 34.0, 106.0, 110.0, 97.0, 80.0, 89.0, 64.0, 150.0, 154.0, 107.0, 83.0, 108.0, 47.0, 159.0, 1.0, 63.0, 129.0, 9.0, 163.0, 53.0, 79.0, 18.0, 123.0, 127.0, 81.0, 27.0, 48.0, 151.0, 68.0, 52.0, 76.0, 57.0, 71.0, 139.0, 105.0, 51.0, 24.0, 143.0, 156.0, 61.0, 50.0, 119.0, 66.0, 12.0, 161.0, 21.0, 133.0, 22.0, 138.0, 41.0, 30.0, 67.0, 144.0, 29.0, 126.0, 115.0, 40.0, 131.0, 39.0, 100.0, 135.0, 167.0, 113.0, 141.0, 142.0, 158.0, 44.0, 117.0, 147.0, 42.0, 35.0, 87.0, 109.0, 33.0, 112.0, 153.0, 125.0, 121.0, 11.0, 157.0, 114.0, 168.0, 134.0, 85.0, 2.0, 4.0, 103.0, 145.0, 88.0, 94.0, 160.0, 7.0, 6.0, 8.0, 75.0, 102.0, 90.0, 84.0, 59.0, 19.0, 62.0, 165.0, 38.0, 58.0, 43.0, 10.0, 96.0, 132.0, 37.0, 16.0, 69.0, 54.0, 56.0, 45.0, 152.0, 164.0, 82.0, 111.0, 140.0, 13.0, 70.0, 55.0, 20.0, 23.0, 118.0, 162.0, 15.0, 86.0, 46.0, 3.0, 25.0, 146.0, 130.0, 120.0, 77.0, 122.0, 36.0, 28.0, 124.0, 166.0, 99.0, 136.0, 137.0, 101.0, 31.0, 17.0, 26.0, 95.0, 72.0, 93.0, 92.0, 116.0, 32.0, 91.0, 60.0, 148.0, 73.0]):
                            # print(i)
                            # print(len(station_labels))
                            station = f'Sta{int(key)}'
                            station_labels_ = [0,0,0,0,0]
                            station_labels_[station_labels[i]] = 1
                            x_train_part.extend(station_labels_)
                            # print(x_train_dict.get(int(key), [0., 0.]))
                            info = stationinfo_dict.get(station)
                            x_train_part.append(int(info[1]))
                            which_line = [0,0,0,0,0,0,0,0]
                            which_line[line_names_dict[info[0]]] = 1
                            x_train_part.extend(which_line)
                            x_train_part.extend(x_train_dict.get(int(key), [0., 0., 0., 0.]))
                        x_train.append(x_train_part)
        print(len(x_train[0]))

        with open('data/list1_flow.csv','w',newline='') as f3:
            f3_csv = csv.writer(f3)
            f3_csv.writerows(x_train)
        # with open('list1_in_flow_plusX.csv','w',newline='') as f3:
        #     f3_csv = csv.writer(f3)
        #     f3_csv.writerows(y_train)

    def getData(self):
        G = self.getGraph()
        result = self.getFlow()

def main():
    db = PreProcess()
    db.getData()


if __name__ == '__main__':
    main()

"""在那个某车站突然涌入大量人群时
你们想做的显示效果
当今天晚些时候会有学校放假等现象时, 在早些时候用户为注入参数更改预测走势

1. 把预测数据存入数据库
2. 在突然加入大量人群时, 先推测出其流动方向比例, 得出断面流量增加值
2. 再次带入list3_pre中预测"""