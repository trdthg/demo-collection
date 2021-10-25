import pandas as pd

a = pd.DataFrame(pd.read_csv('./data/weather.csv', encoding='gbk'))
b = a['天气状况']
b = set(b)
c = []
for a in b:
    c.extend(a.split(' /'))
print(set(c))
