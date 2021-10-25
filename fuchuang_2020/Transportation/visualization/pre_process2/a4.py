import pandas as pd
import numpy as np

workday = pd.DataFrame(pd.read_csv('./small_workday.csv', encoding='gbk'))
workday.drop(['sss'], axis=1)
workday.to_csv('./small_workday.csv')