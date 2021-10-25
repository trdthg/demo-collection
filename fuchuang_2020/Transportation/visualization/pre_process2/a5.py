import pandas  as pd
import numpy as np
import multiprocessing as mp
print()
# 直接读取

trips = pd.DataFrame(pd.read_csv('./small_trips.csv')) # 加上header=1能忽略第一行
workday = pd.DataFrame(pd.read_csv('./small_workday.csv'))
workday = workday.drop(['year'], axis=1)
workday = workday.drop(['Column1'], axis=1)

trips['dayprop'] = '0'

for index, row in trips.iterrows():
    flag = 0
    for index_, row_ in workday.iterrows():
        if row[0] == row_[1] and row[1]==row_[2]:
            flag = 1
            trips.iloc[index,2] = row_[0]
            print(index)
            break
    if flag == 0:
        trips.iloc[index,2] = 1
trips.to_csv('./part1_trips.csv')
# df = trips['inmonth']
# df = pd.DataFrame(df)
# df['inday'] = trips['inday']
# df.to_csv('./small_trips.csv')    

    

