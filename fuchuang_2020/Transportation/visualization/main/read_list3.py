
import time
import csv

import pymysql
import numpy as np
import scipy.sparse as sp
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

import graph2
import shortestpass
from pyasn1.type.univ import Null

lr = 0.01
dropout = 0
verbose = 1
epochs = 30
weight_decay = 5e-4

def main():
    db = PreProcess()
    db.getData()

class PreProcess():

    def __init__(self, library="library_flow"):
        super().__init__()
        print('-'*100)
        self.dbconnect(library)
        reader = shortestpass.ReadFile()
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
        # G=nx.Graph(graph_dict)
        # G_mat = nx.adjacency_matrix(G)
        # plt.figure()
        # nx.draw(G,with_labels=True,node_size=50,node_color='r',width=0.1,edge_color='r',font_color=None,font_size=6)

        # 得到以边为节点的临接矩阵
        self.graph_dict = graph_dict
        new_dict = {}
        for key in graph_dict.keys():
            one_connection = []
            for item in graph_dict[key]:
                one_connection.append((key, item))
            for item in one_connection:
                new_dict[(item[1],item[0])] = [a for a in one_connection if a != item]
        graph_dict = new_dict

        G=nx.Graph(graph_dict)
        print(G.nodes.data())
        self.normal_list = [item[0][0]*100 + item[0][1] for item in G.nodes.data()]
        G_mat = nx.adjacency_matrix(G)
        print(type(G_mat))
        print(G_mat.toarray())
        with open('list3_G.csv','w',newline='') as f3:
            f3_csv = csv.writer(f3)
            f3_csv.writerows(G_mat.toarray())
        print('list3_G.shape', G_mat.shape)
        # plt.figure()
        # nx.draw(G,with_labels=True,node_size=50,node_color='r',width=0.1,edge_color='r',font_color=None,font_size=6)
        # plt.show()
        return G

    def getFlow(self):
    
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
                for hour in range(9, 22):
                    for minute in range(0, 2):
                        x_train_part, y_train_part = [], []

                        time_start = f'{day}:{hour}:{30*minute}'
                        sql = f'SELECT station_1, station_2, flow FROM list3_{month} WHERE time_start = "{time_start}"'
                        self.cursor.execute(sql)
                        # 获取某一时段的流量原始数据
                        a = self.cursor.fetchall()
                        already_in_stations = []
                        staflow = []
                        x_train_dict, y_train_dict = {}, {}
                        for row in a:
                            already_in_stations.append(100 * float(row[0][3:]) + float(row[1][3:]))
                            x_train_dict[100 * float(row[0][3:]) + float(row[1][3:])] = row[2]
                        for key in self.normal_list:
                            x_train_part.append(x_train_dict.get(key, 0.))
                        print(x_train_part)
                        x_train.append(x_train_part)
        print(len(x_train[0]))

        with open('list3_flow.csv','w',newline='') as f3:
            f3_csv = csv.writer(f3)
            f3_csv.writerows(x_train)

                    
        print('-'*100)
        print('len(x,y _train)', len(x_train))

    def getData(self):
        G = self.getGraph()
        self.getFlow()

if __name__ == '__main__':
    main()