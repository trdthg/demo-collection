
import os, json, csv, calendar
import pandas  as pd
# import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
# import shortestpass
import graph2 
import pymysql
from pymysql.converters import escape_string
from functools import partial
from tqdm import tqdm
import time
transfer_stations = ['Sta89', 'Sta127', 'Sta41', 'Sta134', 'Sta3', 'Sta15', 'Sta140', 'Sta75', 'Sta90', 'Sta47', 'Sta23', 'Sta56', 'Sta115', 'Sta63', 'Sta114', 'Sta135', 'Sta87']

allstations = ['Sta65', 'Sta49', 'Sta149', 'Sta74', 'Sta128', 'Sta34', 'Sta106', 'Sta110', 'Sta97', 'Sta80', 'Sta89', 'Sta64', 'Sta150', 'Sta154', 'Sta107', 'Sta83', 'Sta108', 'Sta159', 'Sta1', 'Sta129', 'Sta9', 'Sta163', 'Sta53', 'Sta79', 'Sta18', 'Sta47', 'Sta123', 'Sta127', 'Sta81', 'Sta27', 'Sta48', 'Sta151', 'Sta68', 'Sta52', 'Sta76', 'Sta57', 'Sta71', 'Sta139', 'Sta105', 'Sta51', 'Sta24', 'Sta143', 'Sta156', 'Sta61', 'Sta50', 'Sta119', 'Sta66', 'Sta12', 'Sta161', 'Sta21', 'Sta133', 'Sta22', 'Sta138', 'Sta41', 'Sta30', 'Sta67', 'Sta144', 'Sta29', 'Sta126', 'Sta40', 'Sta131', 'Sta39', 'Sta100', 'Sta167', 'Sta113', 'Sta141', 'Sta142', 'Sta158', 'Sta44', 'Sta117', 'Sta147', 'Sta42', 'Sta35', 'Sta109', 'Sta33', 'Sta112', 'Sta153', 'Sta125', 'Sta121', 'Sta11', 'Sta157', 'Sta114', 'Sta168', 'Sta135', 'Sta134', 'Sta85', 'Sta2', 'Sta4', 'Sta103', 'Sta145', 'Sta88', 'Sta87', 'Sta94', 'Sta160', 'Sta7', 'Sta6', 'Sta8', 'Sta75', 'Sta102', 'Sta84', 'Sta59', 'Sta19', 'Sta62', 'Sta165', 'Sta38', 'Sta58', 'Sta43', 'Sta10', 'Sta96', 'Sta132', 'Sta37', 'Sta16', 'Sta69', 'Sta54', 'Sta77', 'Sta122', 'Sta36', 'Sta28', 'Sta124', 'Sta166', 'Sta99', 'Sta45', 'Sta152', 'Sta164', 'Sta82', 'Sta111', 'Sta140', 'Sta13', 'Sta70', 'Sta55', 'Sta20', 'Sta23', 'Sta56', 'Sta118', 'Sta115', 'Sta162', 'Sta15', 'Sta86', 'Sta46', 'Sta3','Sta63',  'Sta25', 'Sta146', 'Sta130', 'Sta120', 'Sta136', 'Sta137', 'Sta101', 'Sta31', 'Sta17', 'Sta26', 'Sta90', 'Sta95', 'Sta72', 'Sta93', 'Sta92', 'Sta116', 'Sta32', 'Sta91', 'Sta60', 'Sta148', 'Sta73']


class DB():
    
    def __init__(self, DB):
        DB_USER = 'maker0'
        DB_PASS = 'Maker0000'
        DB_HOST = 'rm-bp11labi01950io698o.mysql.rds.aliyuncs.com'
        DB_PORT = 3306
        DATABASE = DB
        try:
            self.connect_info = pymysql.connect(user=DB_USER, passwd=DB_PASS, host=DB_HOST, port=DB_PORT, db=DATABASE)  #1
            self.cursor = self.connect_info.cursor()
            for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
                table_name_1 = f'list1_{month}'
                table_name_2 = f'list2_{month}'
                table_name_3 = f'list3_{month}'
                table_name_4 = f'list4_{month}'
                sql1 = f"""CREATE TABLE IF NOT EXISTS {table_name_1} (
                        station  CHAR(20) NOT NULL,
                        in_flow FLOAT,
                        out_flow FLOAT,
                        in_flow_plus FLOAT,
                        out_flow_plus FLOAT,
                        time_start CHAR(20) NOT NULL )"""
                sql2 = f"""CREATE TABLE IF NOT EXISTS {table_name_2} (
                        station_in  CHAR(20) NOT NULL,
                        station_out  CHAR(20) NOT NULL,
                        flow FLOAT,
                        flow_plus FLOAT,
                        time_start CHAR(20) NOT NULL )"""
                sql3 = f"""CREATE TABLE IF NOT EXISTS {table_name_3} (
                        station_1  CHAR(20) NOT NULL,
                        station_2  CHAR(20) NOT NULL,
                        flow FLOAT,
                        time_start CHAR(20) NOT NULL )"""
                sql4 = f'''CREATE TABLE IF NOT EXISTS {table_name_4}  (
                        linename CHAR(20) NOT NULL,
                        flow FLOAT,
                        time_start CHAR(20) NOT NULL )'''
                self.cursor.execute(sql1)
                self.cursor.execute(sql2)
                self.cursor.execute(sql3)
                self.cursor.execute(sql4)
        except pymysql.Error as e:
            raise e
    
    def close(self):
        self.connect_info.close()
db = DB('library_flow')

def write_list_to_json(list, json_file_name, json_file_save_path):
    os.chdir(json_file_save_path)
    with open(json_file_name, 'w', encoding='utf-8') as  f:
        json.dump(list, f)

def main():
    time_start = time.time()
    global db
    trips = pd.DataFrame(pd.read_csv('./data/new_trips.csv'))
    stations = pd.DataFrame(pd.read_csv('./data/station.csv', encoding='gbk'))
    flow = {}
    aaa = []
    for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
        year = 2020
        res = calendar.monthrange(year, month)
        df = pd.DataFrame(trips.loc[trips['inmonth'] == month])
        for day in range(1, res[1]):
            print(day)
            df_day = df.loc[df['inday'] == day]
            for hour in range(6,23):
                df_day_hour = df_day.loc[df_day['inhour']==hour]
                interval = 30
                time_table = [turn*interval for turn in range(int(60/interval))]
                for i, minute in enumerate(time_table):
                    df_day_hour_minute = df_day_hour.loc[(df_day_hour['inminute']<time_table[i]+interval) & (df_day_hour['inminute']>=time_table[i])]
                    aaa.append([df_day_hour_minute, month, day, hour, minute])
    # for item in aaa:
    #     job(item)
        pool = mp.Pool(processes=8) 
        re = pool.map(job, aaa)
        # db.connect_info.commit()
        db.connect_info.close()
        break

                    # break
                # break
        #     break
        # break
    print(time.time()-time_start)

def job(df):
    global db
    month = df[1]
    day = df[2]
    hour = df[3]
    minute = df[4]
    df = df[0]
    print(month,day)
    # db = DB('library_flow', month, day)
    time = escape_string(f'{day}:{hour}:{minute}')
    temp, temp2, temp3, temp4 = {}, {}, {}, {}
    transfer_stations_temp, transfer_stations_temp2 = {}, {}
    for index, row in df.iterrows():
        # print(index)
        stain, staout = row[2], row[4]
        if stain == staout :
            continue
        if stain not in allstations and staout not in allstations:
            continue
        
        # 1.
        if stain in temp.keys():
            temp[stain][0] += 1
        else:
            temp[stain] = [1, 0]
        if staout in temp.keys():
            temp[staout][1] += 1
        else:
            temp[staout] = [0, 1]
        # 2.
        if (stain, staout) in temp2.keys():
            temp2[(stain,staout)] += 1
        else:
            temp2[(stain,staout)] = 1
        try:
            graph_object = graph2.Dfs()
            big_list = graph_object.getPassInfo(stain, staout)
        except:
            continue
        for small_list in big_list:      
            # 遍历所有站点 
            for i in range(len(small_list[0])):
                if i!=0 and i!=len(small_list[0]):
                    if small_list[0][i] in transfer_stations:
                        # 1_2
                        if small_list[0][i] in transfer_stations_temp.keys():
                            transfer_stations_temp[small_list[0][i]] += 1*small_list[-1]
                        else:
                            transfer_stations_temp[small_list[0][i]] = 1*small_list[-1]
                # 3
                if i != len(small_list[0])-1:
                    if (small_list[0][i], small_list[0][i+1]) in temp3.keys():
                        temp3[(small_list[0][i], small_list[0][i+1])] += 1*small_list[-1]
                    else:
                        temp3[(small_list[0][i], small_list[0][i+1])] = 1*small_list[-1]
        # 2_2
        for small_list in big_list:
            ods = small_list[2]
            if ods==[]:
                if (stain, staout) in transfer_stations_temp2.keys():
                    transfer_stations_temp2[(stain, staout)] += 1*small_list[-1]
                else:
                    transfer_stations_temp2[stain, staout] = 1*small_list[-1]
            else:
                for od in ods:
                    if od in transfer_stations_temp2.keys():
                        transfer_stations_temp2[od] += 1*small_list[-1]
                    else:
                        transfer_stations_temp2[od] = 1*small_list[-1]
        # 4_1 线路客流量
        for small_list in big_list:
            lines = small_list[4]
            rate = small_list[-1]
            # print(lines, rate)
            for line in lines:
                if line in temp4.keys():
                    temp4[line] += 1*rate
                else:
                    temp4[line] = 1*rate

    # 1_2
    for key in temp.keys():
        temp[key].extend(temp[key])
    for key in transfer_stations_temp.keys():
        if key in temp.keys():
            temp[key][2] = (temp[key][0] + transfer_stations_temp[key])
            temp[key][3] = (temp[key][1] + transfer_stations_temp[key])
        else:
            temp[key]=[0, 0 , transfer_stations_temp[key], transfer_stations_temp[key]]
    # 2_1  
    for key in temp2.keys():
        temp2[key] = [temp2[key], temp2[key]]
    # 2_2
    for key in transfer_stations_temp2.keys():
        try:
            temp2[key][1] = temp2[key] + transfer_stations_temp2[key]
        except:
            temp2[key] = [0 , transfer_stations_temp2[key]]
    for key in temp.keys():
        db.cursor.execute(  f"""INSERT INTO list1_{month} VALUES ('{key}', {temp[key][0]},{temp[key][1]}, {temp[key][2]}, {temp[key][3]},'{time}')""")
    for key in temp2.keys():
        db.cursor.execute(  f"""INSERT INTO list2_{month} VALUES ('{key[0]}', '{key[1]}',{temp2[key][0]}, {temp2[key][1]},'{time}')""")
    for key in temp3.keys():
        db.cursor.execute(  f"""INSERT INTO list3_{month} VALUES ('{key[0]}', '{key[1]}',{temp3[key]},'{time}')""")
    for key in temp4.keys():
        db.cursor.execute(  f"""INSERT INTO list4_{month} VALUES ('{key}', {temp4[key]},'{time}')""")
    db.connect_info.commit()
    
    return 

if __name__=='__main__':
    main()