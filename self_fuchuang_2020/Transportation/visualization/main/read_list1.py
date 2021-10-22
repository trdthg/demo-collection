
import time
import csv

import pymysql
import numpy as np
import scipy.sparse as sp
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

import graph 
import shortestpass
from pyasn1.type.univ import Null

lr = 0.01
dropout = 0
verbose = 1
epochs = 30
weight_decay = 5e-4

def main():
    db = PreProcess()
    # db.getData()
    

class PreProcess():

    def __init__(self, library="library_flow"):
        super().__init__()
        print('-'*100)
        self.dbconnect(library)
        reader = shortestpass.ReadFile()
        self.all_stations = reader.readTxt()
        G = self.getGraph()


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
        with open('G.csv','w',newline='') as f3:
            f3_csv = csv.writer(f3)
            f3_csv.writerows(G_mat.toarray())
        print('G.shape', G_mat.shape)
        nx.draw(G,with_labels=True,node_size=50,node_color='r',width=0.1,edge_color='r',font_color=None,font_size=6)
        plt.show()
        return G

    def getFlow(self, time_len=12, test_len=4):
        workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))
        workday['date'] = pd.to_datetime(workday['Column1'],format="%Y%m%d")
        # 2. 得到 X (特征矩阵)

        # x_train为进站流量信息, y_train包含了[进站流量, 线路流量, 断面流量]
        # 故一个batch要以一个时段的进站流量为单位
        x_train, y_train = [], []
        for month in (3,4,5,6):
            for day in range(1, 29):
                # 得到是否是节假日
                dayprop = np.array(workday.loc[(workday['date'].dt.month==month) & (workday['date'].dt.day==day)]['Column2'])[0]
                print('dayprop', dayprop)
                for hour in range(7, 22):
                    for minute in range(0, 2):
                        x_train_part, y_train_part = [], []

                        time_start = f'{day}:{hour}:{30*minute}'
                        sql = f'SELECT station, in_flow, in_flow_plus FROM list1_{month} WHERE time_start = "{time_start}"'
                        self.cursor.execute(sql)
                        # 获取某一时段的流量原始数据
                        a = self.cursor.fetchall()
                        already_in_stations = []
                        staflow = []
                        x_train_dict, y_train_dict = {}, {}
                        for row in a:
                            already_in_stations.append(row[0])
                            x_train_dict[float(row[0][3:])] = row[1]
                            y_train_dict[float(row[0][3:])] = row[2]
                        for key in [65.0, 49.0, 149.0, 74.0, 128.0, 34.0, 106.0, 110.0, 97.0, 80.0, 89.0, 64.0, 150.0, 154.0, 107.0, 83.0, 108.0, 47.0, 159.0, 1.0, 63.0, 129.0, 9.0, 163.0, 53.0, 79.0, 18.0, 123.0, 127.0, 81.0, 27.0, 48.0, 151.0, 68.0, 52.0, 76.0, 57.0, 71.0, 139.0, 105.0, 51.0, 24.0, 143.0, 156.0, 61.0, 50.0, 119.0, 66.0, 12.0, 161.0, 21.0, 133.0, 22.0, 138.0, 41.0, 30.0, 67.0, 144.0, 29.0, 126.0, 115.0, 40.0, 131.0, 39.0, 100.0, 135.0, 167.0, 113.0, 141.0, 142.0, 158.0, 44.0, 117.0, 147.0, 42.0, 35.0, 87.0, 109.0, 33.0, 112.0, 153.0, 125.0, 121.0, 11.0, 157.0, 114.0, 168.0, 134.0, 85.0, 2.0, 4.0, 103.0, 145.0, 88.0, 94.0, 160.0, 7.0, 6.0, 8.0, 75.0, 102.0, 90.0, 84.0, 59.0, 19.0, 62.0, 165.0, 38.0, 58.0, 43.0, 10.0, 96.0, 132.0, 37.0, 16.0, 69.0, 54.0, 56.0, 45.0, 152.0, 164.0, 82.0, 111.0, 140.0, 13.0, 70.0, 55.0, 20.0, 23.0, 118.0, 162.0, 15.0, 86.0, 46.0, 3.0, 25.0, 146.0, 130.0, 120.0, 77.0, 122.0, 36.0, 28.0, 124.0, 166.0, 99.0, 136.0, 137.0, 101.0, 31.0, 17.0, 26.0, 95.0, 72.0, 93.0, 92.0, 116.0, 32.0, 91.0, 60.0, 148.0, 73.0]:
                            x_train_part.append(x_train_dict.get(key, 0.))
                            y_train_part.append(y_train_dict.get(key, 0.))
                        print(type(x_train_part))
                        x_train.append(x_train_part)
                        y_train.append(y_train_part)
        print(len(x_train[0]))

        with open('list1_in_flow.csv','w',newline='') as f3:
            f3_csv = csv.writer(f3)
            rows = []
            # for i in range(len(x_train)-time_len-test_len):
                # rows.append(x_train[i:i+time_len+test_len])
            f3_csv.writerows(x_train)
        with open('list1_in_flow_plus.csv','w',newline='') as f3:
            f3_csv = csv.writer(f3)
            rows = []
            # for i in range(len(y_train)-time_len-test_len):
            #     rows.append(y_train[i:i+time_len+test_len])
            f3_csv.writerows(y_train)
                    
        print('-'*100)
        print('len(x,y _train)', len(y_train), len(x_train))
        return [x_train, y_train]

  


if __name__ == '__main__':
    main()