
import os, json, csv, calendar
import pandas  as pd
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp
# import shortestpass
import graph 
import pymysql
from pymysql.converters import escape_string
from functools import partial

transfer_stations = ['Sta89', 'Sta127', 'Sta41', 'Sta134', 'Sta3', 'Sta15', 'Sta140', 'Sta75', 'Sta90', 'Sta47', 'Sta23', 'Sta56', 'Sta115', 'Sta63', 'Sta114', 'Sta135', 'Sta87']

allstations = ['Sta65', 'Sta49', 'Sta149', 'Sta74', 'Sta128', 'Sta34', 'Sta106', 'Sta110', 'Sta97', 'Sta80', 'Sta89', 'Sta64', 'Sta150', 'Sta154', 'Sta107', 'Sta83', 'Sta108', 'Sta159', 'Sta1', 'Sta129', 'Sta9', 'Sta163', 'Sta53', 'Sta79', 'Sta18', 'Sta47', 'Sta123', 'Sta127', 'Sta81', 'Sta27', 'Sta48', 'Sta151', 'Sta68', 'Sta52', 'Sta76', 'Sta57', 'Sta71', 'Sta139', 'Sta105', 'Sta51', 'Sta24', 'Sta143', 'Sta156', 'Sta61', 'Sta50', 'Sta119', 'Sta66', 'Sta12', 'Sta161', 'Sta21', 'Sta133', 'Sta22', 'Sta138', 'Sta41', 'Sta30', 'Sta67', 'Sta144', 'Sta29', 'Sta126', 'Sta40', 'Sta131', 'Sta39', 'Sta100', 'Sta167', 'Sta113', 'Sta141', 'Sta142', 'Sta158', 'Sta44', 'Sta117', 'Sta147', 'Sta42', 'Sta35', 'Sta109', 'Sta33', 'Sta112', 'Sta153', 'Sta125', 'Sta121', 'Sta11', 'Sta157', 'Sta114', 'Sta168', 'Sta135', 'Sta134', 'Sta85', 'Sta2', 'Sta4', 'Sta103', 'Sta145', 'Sta88', 'Sta87', 'Sta94', 'Sta160', 'Sta7', 'Sta6', 'Sta8', 'Sta75', 'Sta102', 'Sta84', 'Sta59', 'Sta19', 'Sta62', 'Sta165', 'Sta38', 'Sta58', 'Sta43', 'Sta10', 'Sta96', 'Sta132', 'Sta37', 'Sta16', 'Sta69', 'Sta54', 'Sta77', 'Sta122', 'Sta36', 'Sta28', 'Sta124', 'Sta166', 'Sta99', 'Sta45', 'Sta152', 'Sta164', 'Sta82', 'Sta111', 'Sta140', 'Sta13', 'Sta70', 'Sta55', 'Sta20', 'Sta23', 'Sta56', 'Sta118', 'Sta115', 'Sta162', 'Sta15', 'Sta86', 'Sta46', 'Sta3','Sta63',  'Sta25', 'Sta146', 'Sta130', 'Sta120', 'Sta136', 'Sta137', 'Sta101', 'Sta31', 'Sta17', 'Sta26', 'Sta90', 'Sta95', 'Sta72', 'Sta93', 'Sta92', 'Sta116', 'Sta32', 'Sta91', 'Sta60', 'Sta148', 'Sta73']

class DB():
    
    def __init__(self, DB, month, day):
        DB_USER = 'maker0'
        DB_PASS = 'Maker0000'
        DB_HOST = 'rm-bp11labi01950io698o.mysql.rds.aliyuncs.com'
        DB_PORT = 3306
        DATABASE = DB
        try:
            self.connect_info = pymysql.connect(user=DB_USER, passwd=DB_PASS, host=DB_HOST, port=DB_PORT, db=DATABASE)  #1
            self.cursor = self.connect_info.cursor()
            # 查询语句，选出testexcel表中的所有数据
            # sql = """select * from trips"""
            # read_sql_query的两个参数: sql语句， 数据库连接
            # df = pd.read_sql_query(sql,con=self.connect_info)
            # 输出testexcel表的查询结果
            # print('连接成功')
            table_name_1 = f'list1_{month}_{day}'
            table_name_2 = f'list2_{month}_{day}'
            table_name_3 = f'list3_{month}_{day}'
            table_name_4 = f'list4_{month}_{day}'
            # print(table_name)
            # self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            # 使用预处理语句创建表
            sql1 = f"""CREATE TABLE {table_name_1} (
                    station  CHAR(20) NOT NULL,
                    in_flow FLOAT,
                    out_flow FLOAT,
                    in_flow_plus FLOAT,
                    out_flow_plus FLOAT,
                    time_start CHAR(20) NOT NULL )"""
            sql2 = f"""CREATE TABLE {table_name_2} (
                    station_in  CHAR(20) NOT NULL,
                    station_out  CHAR(20) NOT NULL,
                    flow FLOAT,
                    flow_plus FLOAT,
                    time_start CHAR(20) NOT NULL )"""
            sql3 = f"""CREATE TABLE {table_name_3} (
                    station_1  CHAR(20) NOT NULL,
                    station_2  CHAR(20) NOT NULL,
                    flow FLOAT,
                    time_start CHAR(20) NOT NULL )"""
            sql4 = f'''CREATE TABLE {table_name_4}  (
                    linename CHAR(20) NOT NULL,
                    flow FLOAT,
                    time_start CHAR(20) NOT NULL )'''
            try: self.cursor.execute(sql1)
            except: pass
            try: self.cursor.execute(sql2)
            except: pass
            try: self.cursor.execute(sql3)
            except: pass
            try: self.cursor.execute(sql4)
            except: pass

        except pymysql.Error as e:
            print("数据库连接失败")
            raise e
    

def write_list_to_json(list, json_file_name, json_file_save_path):
    os.chdir(json_file_save_path)
    with open(json_file_name, 'w', encoding='utf-8') as  f:
        json.dump(list, f)

def main():
    # b = DB('library_flow')
    trips = pd.DataFrame(pd.read_csv('./data/new_trips.csv'))
    stations = pd.DataFrame(pd.read_csv('./data/station.csv', encoding='gbk'))

    year = 2020
    flow = {}  
    for month in [7,1,2,3,4,5,6,7,8,12]:
        # 获取该月的所有trips数据
        res = calendar.monthrange(year,month)
        df = pd.DataFrame(trips.loc[trips['inmonth'] == month])
        for day in range(1, res[1]):
            # 获取该天的所有trips数据
            df_day = df.loc[df['inday'] == day]
            aaa = []
            for hour in range(6,23):
                df_day_hour = df_day.loc[df_day['inhour']==hour]
                for minute in [0,30]:
                    df_day_hour_minute = df_day_hour.loc[(df_day_hour['inminute']<30+minute) & (df_day_hour['inminute']>=0+minute)]
                    aaa.append([df_day_hour_minute, month, day, hour, minute])
                    # print(f'{month}月{day}日 {hour}:{minute}')
    # partial_work = partial(job, month=month, day=day, hour=hour, minute=minute)
    # re = pool.map(partial_work, aaa)
            pool = mp.Pool(processes=8) # 定义CPU核数量为3
            re = pool.map(job, aaa)
            print(re)
                    # job(df_day_hour_minute, hour, minute)
                    # break
                # break
            break
        break

def job(df):
    month = df[1]
    day = df[2]
    hour = df[3]
    minute = df[4]
    df = df[0]
    list1_1,list1_2,list2_1,list2_2,list3,list4 = [],[],[],[],[],[]
    temp, temp2, temp3, temp4 = {}, {}, {}, {}
    transfer_stations_temp, transfer_stations_temp2 = {}, {}
    
    for index, row in df.iterrows():
        # print(index)
        stain, staout = row[2], row[4]
        
        if stain in allstations and staout in allstations:
            pass
        else:
            continue
        # 1.
        if stain == staout :
            continue
        if stain in temp.keys():
            temp[stain][0] += 1
        else:
            temp[stain] = [1, 0]
        if staout in temp.keys():
            temp[staout][1] += 1
        else:
            temp[staout] = [0, 1]
        # print(temp)
        # 2.
        if (stain, staout) in temp2.keys():
            temp2[(stain,staout)] += 1
        else:
            temp2[(stain,staout)] = 1
        # 3/4
        # print(stain,staout)
        
        try:

            graph_object = graph.Dfs()
            big_list = graph_object.getPassInfo(stain, staout)
            if big_list[0][-1] > 0:
                # print(big_list[0][-1])
                pass
            else:
                print(big_list)
                continue
            # small_list[0] = shortestpass.main(stain, staout)   
        except:
            continue
        # print(small_list[0])     
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
    
    db = DB('library_flow', month, day)

    # db.cursor.execute("""INSERT INTO list1 VALUES ('Mac', 'Mohan', 20, 'M', 2000)""")

    # 1_1
    a = 0
    # for key in temp.keys():
    #     list1_1.append({'station':key,'in':temp[key][0], 'out':temp[key][1]})
    #     a += temp[key][0]

    # 1_2
    for key in temp.keys():
        temp[key].extend(temp[key])
    for key in transfer_stations_temp.keys():
        if key in temp.keys():
            # temp[key][0] + transfer_stations_temp[key]
            # temp[key][1] + transfer_stations_temp[key]
            temp[key][2] = (temp[key][0] + transfer_stations_temp[key])
            temp[key][3] = (temp[key][1] + transfer_stations_temp[key])
        else:
            # temp[key] = [transfer_stations_temp[key], transfer_stations_temp[key]]
            temp[key]=[transfer_stations_temp[key], transfer_stations_temp[key], transfer_stations_temp[key], transfer_stations_temp[key]]
    for key in temp.keys():
        # if len(temp[key])< 4:

        # print(temp[key])
        list1_2.append({'station':key,'in_flow':temp[key][0], 'out_flow':temp[key][1], 'in_flow_plus':temp[key][2], 'out_flow_plus':temp[key][3]})        
        key = escape_string(key) 
        time = escape_string(f'{hour}:{minute}')
        a = temp[key][0]
        b = temp[key][1]
        c = temp[key][2]
        d = temp[key][3]
        db.cursor.execute(  f"""INSERT INTO list1_{month}_{day} VALUES ('{key}', {a},{b}, {c}, {d},'{time}')""")
        # db.cursor.execute(  f"""INSERT INTO list1_{month}_{day} VALUES ('%s',%f,%f,%f,%f,'%s')""" % (key,8.9,9.8,5.7,7.99,'gfxzgfh'))
    # 2_1  
    for key in temp2.keys():
        # list2_1.append({'stain':key[0], 'staout': key[1], 'flow':temp2[key]})
        temp2[key] = [temp2[key], temp2[key]]
    # 2_2
    for key in transfer_stations_temp2.keys():
        try:
            temp2[key][1] = temp2[key] + transfer_stations_temp2[key]
        except:
            temp2[key] = [transfer_stations_temp2[key], transfer_stations_temp2[key]]
    for key in temp2.keys():
        list2_2.append({'stain':key[0], 'staout': key[1], 'flow':temp2[key]})   
        db.cursor.execute(  f"""INSERT INTO list2_{month}_{day} VALUES ('{key[0]}', '{key[1]}',{temp2[key][0]}, {temp2[key][1]},'{time}')""")

    # 3
    for key in temp3.keys():
        list3.append({'x1':key[0], 'x2': key[1], 'flow':temp3[key]})
        db.cursor.execute(  f"""INSERT INTO list3_{month}_{day} VALUES ('{key[0]}', '{key[1]}',{temp3[key]},'{time}')""")
    
    # 4
    for key in temp4.keys():
        list4.append({'line':temp4[key]})
        db.cursor.execute(  f"""INSERT INTO list4_{month}_{day} VALUES ('{key}', {temp4[key]},'{time}')""")
    db.connect_info.commit()
    db.connect_info.close()
    # k = row[3].split(' ')[1]
    # write_list_to_json(list1_1, f'{k}list1_1.json', './json/')
    # write_list_to_json(list1_2, 'list1_2.json', './')

    # write_list_to_json(list2_1, 'list2_1.json', './')
    # write_list_to_json(list2_2, 'list2_2.json', './')
    
    # write_list_to_json(list3, 'list3.json', './')

    # print(a)
    return a



if __name__=='__main__':
    main()