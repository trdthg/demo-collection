import pandas  as pd
import numpy as np
# 直接读取

trips = pd.DataFrame(pd.read_csv('./data/trips.csv',encoding='gbk')) # 加上header=1能忽略第一行
workday = pd.DataFrame(pd.read_csv('./part1_trips.csv'))
trips = trips.drop(['渠道编号'], axis=1)

trips['进站时间'] = pd.to_datetime(trips['进站时间'],format="%Y/%m/%d %H:%M")
trips['inmonth'] = trips['进站时间'].dt.month
trips['inday'] = trips['进站时间'].dt.day
trips['inhour'] = trips['进站时间'].dt.hour
trips['inminute'] = trips['进站时间'].dt.minute

# trips['出站时间'] = pd.to_datetime(trips['出站时间'],format="%Y/%m/%d %H:%M")
# trips['outyear'] = trips['出站时间'].dt.year
# trips['outmonth'] = trips['出站时间'].dt.month
# trips['outday'] = trips['出站时间'].dt.day

trips['dayofweek'] = trips['进站时间'].dt.dayofweek

# workday['Column1'] = pd.to_datetime(workday['Column1'], format= "%Y-%m-%d")
trips['dayprop'] =  workday['dayprop']
trips.to_csv('./new_trips.csv')