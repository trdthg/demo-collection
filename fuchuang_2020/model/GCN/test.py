import pandas as pd



trips = pd.DataFrame(pd.read_csv('./data/trips.csv', encoding='gbk'))
# trips['det'] = ((pd.to_datetime(trips['出站时间'],format="%Y/%m/%d %H:%M") - pd.to_datetime(trips['进站时间'],format="%Y/%m/%d %H:%M")).dt.total_seconds()/60).astype(int)
dummies = pd.get_dummies(trips['进站名称'])


print(list(dummies.iloc[0,:]))