import pymysql
import datetime
import time
import copy

import pandas as pd
import numpy as np

today = datetime.datetime.today()
year = today.year
young_age = year-35
middle_age = year-60
class DB():
    
    def __init__(self, DB):
        DB_USER = 'maker0'
        DB_PASS = 'Maker0000'
        DB_HOST = 'rm-bp11labi01950io698o.mysql.rds.aliyuncs.com'
        DB_PORT = 3306
        DATABASE = DB
        try:
            self.conn = pymysql.connect(user=DB_USER, passwd=DB_PASS, host=DB_HOST, port=DB_PORT, db=DATABASE)  #1
            self.cursor = self.conn.cursor()
        except:
            pass    
    def close(self):
        self.conn.close()
db = DB('library1')

def createTables(db):
    for table_name in [f'age_map_in', f'age_map_out']:
        sql1 = f"""CREATE TABLE IF NOT EXISTS {table_name} (
            time_start CHAR(20) NOT NULL,
            station  CHAR(20) NOT NULL,
            a1 INT,
            a2 INT,
            a3 INT,
            a4 INT,
            a5 INT,
            a6 INT,
            a7 INT,
            a8 INT,
            a9 INT,
            a10 INT,
            a11 INT,
            a12 INT,
            a13 INT,
            a14 INT,
            a15 INT)"""
        db.cursor.execute(sql1)
    sql1 = f"""CREATE TABLE IF NOT EXISTS trade_money (
            time_start CHAR(20) NOT NULL,
            trade_money INT)"""
    db.cursor.execute(sql1)
# sql = f'SELECT 用户ID, 进站时间, 进站名称, 出站名称, 出站时间 from trips ORDER BY 用户ID'
# db.cursor.execute(sql)
# trips = db.cursor.fetchall()
# sql = f'SELECT 用户ID, 出生年份, 性别 from user ORDER BY 用户ID'
# db.cursor.execute(sql)
# users = db.cursor.fetchall()

# for trip in trips:
#     '进展时间'





# sql = f'SELECT 用户ID from user WHERE 出生年份>{young_age} '
# young = db.cursor.execute(sql)
# print('young',young)
# sql = f'SELECT 用户ID from user WHERE 出生年份>{middle_age} and 出生年份<={young_age}'
# middle = db.cursor.execute(sql)
# print('middle',middle)
# sql = f'SELECT 用户ID from user WHERE 出生年份<={middle_age}'
# old = db.cursor.execute(sql)
# print('old',old)
# a = db.cursor.fetchall()
# for id in a:
#     sql = 'SELECT * FROM trips WHERE 用户ID = "{id}"'
#     db.cursor.execute(sql)
#     b = db.cursor.fetchall()
#     print(f"用户{id}, {len(b)}")

# sql = 'SELECT 用户ID from trips '
# db.cursor.execute(sql)
# a = db.cursor.fetchall()
# print(len(a))
# print(len(set(a)))

allstations = ['全网', 'Sta65', 'Sta49', 'Sta149', 'Sta74', 'Sta128', 'Sta34', 'Sta106', 'Sta110', 'Sta97', 'Sta80', 'Sta89', 'Sta64', 'Sta150', 'Sta154', 'Sta107', 'Sta83', 'Sta108', 'Sta159', 'Sta1', 'Sta129', 'Sta9', 'Sta163', 'Sta53', 'Sta79', 'Sta18', 'Sta47', 'Sta123', 'Sta127', 'Sta81', 'Sta27', 'Sta48', 'Sta151', 'Sta68', 'Sta52', 'Sta76', 'Sta57', 'Sta71', 'Sta139', 'Sta105', 'Sta51', 'Sta24', 'Sta143', 'Sta156', 'Sta61', 'Sta50', 'Sta119', 'Sta66', 'Sta12', 'Sta161', 'Sta21', 'Sta133', 'Sta22', 'Sta138', 'Sta41', 'Sta30', 'Sta67', 'Sta144', 'Sta29', 'Sta126', 'Sta40', 'Sta131', 'Sta39', 'Sta100', 'Sta167', 'Sta113', 'Sta141', 'Sta142', 'Sta158', 'Sta44', 'Sta117', 'Sta147', 'Sta42', 'Sta35', 'Sta109', 'Sta33', 'Sta112', 'Sta153', 'Sta125', 'Sta121', 'Sta11', 'Sta157', 'Sta114', 'Sta168', 'Sta135', 'Sta134', 'Sta85', 'Sta2', 'Sta4', 'Sta103', 'Sta145', 'Sta88', 'Sta87', 'Sta94', 'Sta160', 'Sta7', 'Sta6', 'Sta8', 'Sta75', 'Sta102', 'Sta84', 'Sta59', 'Sta19', 'Sta62', 'Sta165', 'Sta38', 'Sta58', 'Sta43', 'Sta10', 'Sta96', 'Sta132', 'Sta37', 'Sta16', 'Sta69', 'Sta54', 'Sta77', 'Sta122', 'Sta36', 'Sta28', 'Sta124', 'Sta166', 'Sta99', 'Sta45', 'Sta152', 'Sta164', 'Sta82', 'Sta111', 'Sta140', 'Sta13', 'Sta70', 'Sta55', 'Sta20', 'Sta23', 'Sta56', 'Sta118', 'Sta115', 'Sta162', 'Sta15', 'Sta86', 'Sta46', 'Sta3','Sta63',  'Sta25', 'Sta146', 'Sta130', 'Sta120', 'Sta136', 'Sta137', 'Sta101', 'Sta31', 'Sta17', 'Sta26', 'Sta90', 'Sta95', 'Sta72', 'Sta93', 'Sta92', 'Sta116', 'Sta32', 'Sta91', 'Sta60', 'Sta148', 'Sta73']

print("获取数据")
# trips = pd.read_sql('select * from trips;', con=db.conn)
# trips['进站时间'] = pd.to_datetime(trips['进站时间'],format="%Y/%m/%d %H:%M")
# users = pd.read_sql('select * from user;', con=db.conn)
trips = pd.read_csv('./data/trips.csv', encoding='gbk').sort_values(by='用户ID')
trips['进站时间'] = pd.to_datetime(trips['进站时间'],format="%Y/%m/%d %H:%M")
users = pd.read_csv("./data/users.csv", encoding='gbk').sort_values(by='用户ID').reset_index(drop=True)
print(users.head())
print("开辟空间")
in_dict = {}
money_dict = {}
for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
    for day in range(1,30):
        money_dict[f'{month}:{day}'] = 0
        in_dict[f'{month}:{day}'] = {station: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] for station in allstations}
out_dict = copy.deepcopy(in_dict)
# df = pd.DataFrame(trips.loc[(trips['进站时间'].dt.month == month) & (trips['进站时间'].dt.day == day)])
old_id = 0
i = 0
j = 1
sex = 0
print("开始统计")
print(users.loc[i][0],users.loc[1][0],users.loc[2][0],users.loc[3][0],users.loc[4][0],users.loc[5][0])
for trip in trips.itertuples():
    id = trip[1]
    if id == old_id:
        month = trip[3].month
        day = trip[3].day
        stationin = trip[2]
        stationout = trip[4]
        money = trip[7]
        key = f'{month}:{day}'
        try:
            money_dict[key] += money
            if age < 16:
                in_dict[old_key]['全网'][0 + 5*sex] += j
                in_dict[old_key][old_stationin][0 + 5*sex] += j
                in_dict[old_key]['全网'][10] += j
                in_dict[old_key][old_stationin][10] += j
                out_dict[old_key][old_stationout][0 + 5*sex] += j
                out_dict[old_key][old_stationout][10] += j
            elif age < 25:
                in_dict[old_key]['全网'][1 + 5*sex] += j
                in_dict[old_key][old_stationin][1 + 5*sex] += j
                in_dict[old_key]['全网'][11] += j
                in_dict[old_key][old_stationin][11] += j
                out_dict[old_key][old_stationout][1 + 5*sex] += j
                out_dict[old_key][old_stationout][11] += j
            elif age < 40:
                in_dict[old_key]['全网'][2 + 5*sex] += j
                in_dict[old_key][old_stationin][2 + 5*sex] += j
                in_dict[old_key]['全网'][12] += j
                in_dict[old_key][old_stationin][12] += j
                out_dict[old_key][old_stationout][2 + 5*sex] += j
                out_dict[old_key][old_stationout][12] += j
            elif age < 60:
                in_dict[old_key]['全网'][3 + 5*sex] += j
                in_dict[old_key][old_stationin][3 + 5*sex] += j
                in_dict[old_key]['全网'][13] += j
                in_dict[old_key][old_stationin][13] += j
                out_dict[old_key][old_stationout][13] += j
                out_dict[old_key][old_stationout][3 + 5*sex] += j
            else:
                in_dict[old_key]['全网'][4 + 5*sex] += j
                in_dict[old_key][old_stationin][4 + 5*sex] += j
                in_dict[old_key]['全网'][14] += j
                in_dict[old_key][old_stationin][14] += j
                out_dict[old_key][old_stationout][14] += j
                out_dict[old_key][old_stationout][4 + 5*sex] += j
        except:
            pass
    else:
        while(1):
            k = 0
            # print(id , users.loc[i][0])
            while id > users.loc[i][0]:
                k += 1
                i += 1
            if id != users.loc[i][0]:
                break
            old_id = id
            old_month = trip[3].month
            old_day = trip[3].day
            old_stationin = trip[2]
            old_stationout = trip[4]
            old_key = f'{month}:{day}'
            age = 2021 - users.loc[i][2]
            sex = users.loc[i][3]
            print(age, id)
            break

data = []
for day in in_dict.keys():
    for station in in_dict[day].keys():
        k = in_dict[day][station]
        a = [day, station]
        # dict1 = {'time': day, 'station': station}
        # dict2 = {i: k[i] for i in range(15)}
        a.extend([k[i] for i in range(15)])
        # dict1.update(dict2)
        data.append(a)
db = DB('library_flow')
createTables(db)
print(data)
db.cursor.executemany(f"""INSERT INTO age_map_in VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)

data = []
for day in out_dict.keys():
    for station in out_dict[day].keys():
        k = out_dict[day][station]
        # dict1 = {'time': day, 'station': station}
        # dict2 = {i: k[i] for i in range(15)}
        # dict1.update(dict2)
        # data.append(dict1)
        a = [day, station]
        a.extend([k[i] for i in range(15)])
        data.append(a)

db.cursor.executemany(f"""INSERT INTO age_map_out VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)
createTables(db)

data = []
for key in money_dict.keys():
    data.append([key, money_dict[key]])
db.cursor.executemany(f"""INSERT INTO trade_money VALUES (%s,%s)""", data)
db.conn.commit()
