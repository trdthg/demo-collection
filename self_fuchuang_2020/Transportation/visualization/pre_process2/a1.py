import pandas  as pd
import numpy as np

# 直接读取

trips = pd.read_csv('./data/trips.csv',encoding='gbk') # 加上header=1能忽略第一行
trips = pd.DataFrame(trips)
print(type(trips['出站时间'][0]))
trips['出站时间'] = pd.to_datetime(trips['出站时间'],format="%Y/%m/%d %H:%M")
trips['进站时间'] = pd.to_datetime(trips['进站时间'],format="%Y/%m/%d %H:%M")
trips = trips.drop(['渠道编号'], axis=1)
year = trips['进站时间'].dt.year
month = trips['进站时间'].dt.month
print(month)

print( trips.loc[ trips['进站时间'].dt.month == 1 ]['进站时间'].count())  
print( trips.loc[ trips['进站时间'].dt.month == 2 ]['进站时间'].count())  
print( trips.loc[ trips['进站时间'].dt.month == 3 ]['进站时间'].count())  
print( trips.loc[ trips['进站时间'].dt.month == 4 ]['进站时间'].count())  
print( trips.loc[ trips['进站时间'].dt.month == 5 ]['进站时间'].count())  
print( trips.loc[ trips['进站时间'].dt.month == 6 ]['进站时间'].count())  
print( trips.loc[ trips['进站时间'].dt.month == 7 ]['进站时间'].count())  
print( trips.loc[ trips['进站时间'].dt.month == 8 ]['进站时间'].count())  
print( trips.loc[ trips['进站时间'].dt.month == 9 ]['进站时间'].count())  
print( trips.loc[ trips['进站时间'].dt.month == 10 ]['进站时间'].count())  
print( trips.loc[ trips['进站时间'].dt.month == 11]['进站时间'].count())  
print( trips.loc[ trips['进站时间'].dt.month == 12]['进站时间'].count())  