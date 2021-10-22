import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import calendar
trips = pd.DataFrame(pd.read_csv('./data/new_trips.csv'))
stations = pd.DataFrame(pd.read_csv('./data/station.csv', encoding='gbk'))
print(trips)

year = 2020

flow = {}  
'''
flow = {
    1月: {
        1号: {
            sta1:
            sta2:
        }
        2号: {
            sta1:
            sta2:
        }
    }
    2月: {

    }
}
'''
for month in range(1,13):
    flow[month] = {}
    # 获取该月的所有trips数据
    res = calendar.monthrange(year,month)
    df = pd.DataFrame(trips.loc[trips['inmonth'] == month])
    for day in range(1, res[1]):
        # 获取该天的所有trips数据
        df_day = df.loc[df['inday'] == day]
        
        # 统计数据
        sta = df_day.groupby('进站名称').count()['inday']
        sta = dict(zip(sta.index, sta.values))
        flow[month][day] = sta

rows = []
for month in flow.keys():
    for day in flow[month].keys():
        for sta in flow[month][day].keys():
            # print([month, day, sta, flow[month][day][sta]])
            rows.append([month, day, sta, flow[month][day][sta]])
headers = ['month', 'day', 'sta', 'flow']
with open('./sta_flow_by_day.csv','w',newline='', encoding='utf-8') as f2:
    f2_csv = csv.writer(f2)
    f2_csv.writerow(headers)
    f2_csv.writerows(rows)


df = pd.DataFrame(pd.read_csv('./sta_flow_by_day.csv'))
df = df.loc[(df['sta'] == 'Sta1') & (df['month']==2)]
plt.xticks(rotation=270)
plt.bar([f'{month}.{day}' for month, day in zip(np.array(df['month']), np.array(df['day']))], np.array(df['flow']))
plt.show()














routes = {
    '1号线': ['Sta1', 'Sta159', 'Sta108', 'Sta83', 'Sta107', 'Sta154', 'Sta150', 'Sta64', 'Sta89', 'Sta80', 'Sta97', 'Sta110', 'Sta106', 'Sta34', 'Sta128', 'Sta74', 'Sta149', 'Sta49', 'Sta65'], 
    '2号线': ['Sta9', 'Sta163', 'Sta53', 'Sta78', 'Sta79', 'Sta18', 'Sta123', 'Sta127', 'Sta81', 'Sta27', 'Sta48', 'Sta151', 'Sta68', 'Sta52', 'Sta76', 'Sta57', 'Sta71', 'Sta139', 'Sta24', 'Sta105', 'Sta51', 'Sta129', 'Sta47'], 
    '3号线': ['Sta143', 'Sta156', 'Sta61', 'Sta50', 'Sta119', 'Sta66', 'Sta12', 'Sta161', 'Sta21', 'Sta133', 'Sta22', 'Sta138', 'Sta41', 'Sta30', 'Sta67', 'Sta144', 'Sta29', 'Sta126', 'Sta40', 'Sta131', 'Sta39', 'Sta100', 'Sta167', 'Sta113', 'Sta141', 'Sta142', 'Sta158', 'Sta44', 'Sta117', 'Sta147', 'Sta42', 'Sta35', 'Sta109', 'Sta33', 'Sta112', 'Sta153', 'Sta125', 'Sta121', 'Sta11'], 
    '10号线': ['Sta134', 'Sta75', 'Sta157', 'Sta168', 'Sta85', 'Sta2', 'Sta4', 'Sta103', 'Sta145', 'Sta88', 'Sta94', 'Sta160', 'Sta7', 'Sta6', 'Sta8', 'Sta102', 'Sta114', 'Sta135', 'Sta87'], 
    '4号线': ['Sta59', 'Sta19', 'Sta62', 'Sta165', 'Sta58', 'Sta38', 'Sta84'], 
    '5号线': ['Sta43', 'Sta10', 'Sta96', 'Sta132', 'Sta37', 'Sta16', 'Sta69', 'Sta54'], 
    '11号线': ['Sta120', 'Sta130', 'Sta146', 'Sta25', 'Sta3', 'Sta46', 'Sta86', 'Sta15', 'Sta162', 'Sta118', 'Sta20', 'Sta55', 'Sta70', 'Sta13', 'Sta140', 'Sta77', 'Sta122', 'Sta36', 'Sta166', 'Sta99', 'Sta124', 'Sta28', 'Sta82', 'Sta164', 'Sta152', 'Sta45', 'Sta23', 'Sta56', 'Sta115', 'Sta63', 'Sta111'], 
    '12号线': ['Sta136', 'Sta137', 'Sta101', 'Sta17', 'Sta26', 'Sta90', 'Sta95', 'Sta93', 'Sta92', 'Sta32', 'Sta91', 'Sta31', 'Sta72', 'Sta116', 'Sta60', 'Sta148', 'Sta73']
}

sta_flow = {
    '1号线':{},
    '2号线':{},
    '3号线':{},
    '4号线':{},
    '5号线':{},
    '10号线':{},
    '11号线':{},
    '12号线':{},
}



















# with open('./flow__by_month.csv','w',newline='', encoding='utf-8') as f2:
#     f2_csv = csv.writer(f2)
#     f2_csv.writerow(headers)
#     f2_csv.writerows(rows)

