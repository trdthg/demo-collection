import pandas as pd
import csv
import matplotlib.pyplot as plt
trips = pd.DataFrame(pd.read_csv('./data/new_trips.csv'))
# print(trips)
headers = ['route', 'sta', '1','2','3','4','5','6','7','8','9','10','11','12']
rows = []
# 1. all
all_flow = list(trips.groupby('inmonth').count()['inday'])

# row = ['','']
# row += all_flow
# rows.append(row)

print(all_flow)


# 2. pre_for_sta
stas = {}
for i in range(12):
    trips_month = trips.loc[ trips['inmonth']== i+1]
    # trips_month
    sta = trips_month.groupby('进站名称').count()['inday']
    sta = dict(zip(sta.index, sta.values))
    stas[i+1] = sta
# print(stas)

# 3. sta

# stas = {
#     1: {'Sta1': 896, 'Sta10': 28, 'Sta100': 645, 'Sta101': 192,   'Sta115': 1733, 'Sta116': 1},
#     2: {'sta33':345, 'sta43':324,'Sta112': 302, 'Sta113': 206, 'Sta114': 590},
#     3: {'Sta107': 1380, 'Sta108': 2213, 'Sta109': 293, 'Sta11': 71, 'Sta110': 2358, 'Sta111': 188, },
#     4: { 'Sta107': 1380, 'Sta108': 2213, 'Sta109': 293, 'Sta11': 71, 'Sta110': 2358, 'Sta111': 188,}
# }

big_dict = {}
big_dict_gun = {}
with open('./data/station.csv') as f:
        # ['编号', '站点名称', '线路', '行政区域']
        f = csv.reader(f)
        for row in f:
            big_dict[f'{row[1]}'] = {}     
# print(big_dict)    

for key in stas.keys():
    month = stas[key]
    for sta in month.keys():
        try:
            big_dict[sta][key] = month[sta]      
        except:
            try:
                big_dict_gun[sta][key] = month[sta]
            except:
                big_dict_gun[sta] = {}
# print(big_dict)
# print(big_dict_gun)

# 3. sta
print('#-&-$-@-%-'*13)

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

for sta in big_dict.keys():
    sta_value = big_dict[sta]
    for route in routes.keys():
        route_list = routes[route]
        if sta in route_list:
            sta_flow[route][sta] = sta_value
            break

for key in sta_flow.keys():
    print(key)
    for key_ in sta_flow[key].keys():
        print(key_, sta_flow[key][key_])

        row = [key, key_]
        for i in range(1,13):
            if i in sta_flow[key][key_].keys():
                row.append(sta_flow[key][key_][i])
            else:
                row.append(0)
        rows.append(row)
        # sta_flow_film.loc[i] = [key, key_]
    print()


# 4. route
print('#-&-$-@-%-'*13)

route_flow = {
    '1号线':{},
    '2号线':{},
    '3号线':{},
    '4号线':{},
    '5号线':{},
    '10号线':{},
    '11号线':{},
    '12号线':{},
}

for route_key in route_flow.keys():
    for sta_key in sta_flow[route_key]:
        sta = sta_flow[route_key]
        for month_key in sta[sta_key].keys():
            month = sta[sta_key]
            try:
                route_flow[route_key][month_key] += month[month_key]
            except:
                route_flow[route_key][month_key] = month[month_key]

for key in route_flow.keys():
    print(key, route_flow[key])
    
    # row = [key,'']
    # for i in range(1,13):
    #     if i in route_flow[key].keys():
    #         row.append(route_flow[key][i])
    #     else:
    #         row.append(0)
    # rows.append(row)


with open('./flow__by_month.csv','w',newline='', encoding='utf-8') as f2:
    f2_csv = csv.writer(f2)
    f2_csv.writerow(headers)
    f2_csv.writerows(rows)

