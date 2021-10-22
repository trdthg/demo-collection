import pandas  as pd
import numpy as np
import multiprocessing as mp
print()
# 直接读取

trips = pd.DataFrame(pd.read_csv('./data/trips.csv',encoding='gbk')) # 加上header=1能忽略第一行
workday = pd.DataFrame(pd.read_csv('./small_workday.csv'))
trips = trips.drop(['渠道编号'], axis=1)
workday = workday.drop(['year'], axis=1)

trips['进站时间'] = pd.to_datetime(trips['进站时间'],format="%Y/%m/%d %H:%M")
 

# trips['出站时间'] = pd.to_datetime(trips['出站时间'],format="%Y/%m/%d %H:%M")
# trips['outyear'] = trips['出站时间'].dt.year
# trips['outmonth'] = trips['出站时间'].dt.month
# trips['outday'] = trips['出站时间'].dt.day

trips['dayofweek'] = trips['进站时间'].dt.dayofweek

workday['Column1'] = pd.to_datetime(workday['Column1'], format= "%Y-%m-%d")
workday['month'] =  workday['Column1'].dt.month
workday['day'] =  workday['Column1'].dt.day

trips['dayprop'] = '0'

for index, row in trips.iterrows():
    flag = 0
    for index_, row_ in workday.iterrows():
        if row[6] == row_[2] and row[7]==row_[3]:
            flag = 1
            trips.iloc[index,9] = row_[1]
            print(index)
            break
    if flag == 0:
        trips.iloc[index,9] = 1
trips.to_csv('./new_trips.csv')
# df = trips['inmonth']
# df = pd.DataFrame(df)
# df['inday'] = trips['inday']
# df.to_csv('./small_trips.csv')    

    

