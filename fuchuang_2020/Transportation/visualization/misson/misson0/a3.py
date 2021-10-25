import pandas as pd
sta_flow_film = pd.DataFrame(columns=['route', 'sta', '1','2','3','4','5','6','7','8','9','10','11','12'])
# new_empty_row = pd.Series([], index=['A', 'B', 'C', 'D'])
for i in range(9):
    sta_flow_film.append([1, 2,3], i)
sta_flow_film.to_csv('./ssssss.csv')
print(sta_flow_film)