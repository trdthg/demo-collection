
import pandas as pd
import numpy as np

workday = pd.DataFrame(pd.read_csv('./data/workdays2020.csv', encoding='gbk'))

workday['Column1'] = pd.to_datetime(workday['Column1'], format= "%Y%m%d")
workday['year'] =  workday['Column1'].dt.year
workday['month'] =  workday['Column1'].dt.month
workday['day'] =  workday['Column1'].dt.day

print(workday)
# df = pd.DataFrame(
    # columns=['date', 'dayprop', 'year', 'month', 'day']
# )#创建一个数据表格
# print(df)
print(workday['Column2'], type(workday['Column2'][0]))
df = workday.loc[ (workday['Column2'] == '2') |  (workday['Column2'] == '3')]
df = pd.DataFrame(df)
print(df)
df.to_csv('./small_workday.csv')