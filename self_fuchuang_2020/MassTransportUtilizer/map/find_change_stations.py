import csv 

datadict = {
    '1号线': ['Sta65', '3',  'Sta49', '4',  'Sta149', '4', 'Sta74', '4',  'Sta128', '7', 'Sta34', '3', 'Sta106', '4', 'Sta110', '4', 'Sta97', '3', 'Sta80', '3', 'Sta89', '2', 'Sta64', '3', 'Sta150', '4', 'Sta154', '3', 'Sta107', '3', 'Sta83', '3', 'Sta108', '5', 'Sta159', '5', 'Sta1', '30'], 
    '2号线': ['Sta129', '3', 'Sta9', '3',   'Sta163', '3', 'Sta53', '3',  'Sta78', '5', 'Sta79', '3', 'Sta18', '4', 'Sta47', '3', 'Sta123', '3', 'Sta127', '3', 'Sta81', '3', 'Sta27', '3', 'Sta48', '4', 'Sta151', '5', 'Sta68', '3', 'Sta52', '3', 'Sta76', '4', 'Sta57', '6', 'Sta71', '5', 'Sta139', '7', 'Sta105', '6', 'Sta51', '10', 'Sta24', '55'], 
    '3号线': ['Sta143', '4', 'Sta156', '4', 'Sta61', '3',  'Sta50', '4',  'Sta119', '6', 'Sta66', '4', 'Sta12', '4', 'Sta161', '4', 'Sta21', '4', 'Sta133', '3', 'Sta22', '3', 'Sta138', '4', 'Sta41', '4', 'Sta30', '2', 'Sta67', '3', 'Sta144', '9', 'Sta29', '2', 'Sta126', '6', 'Sta40', '3', 'Sta131', '3', 'Sta39', '3', 'Sta100', '4', 'Sta167', '4', 'Sta113', '3', 'Sta141', '4', 'Sta142', '4', 'Sta158', '3', 'Sta44', '3', 'Sta117', '4', 'Sta147', '5', 'Sta42', '3', 'Sta35', '4', 'Sta109', '5', 'Sta33', '4', 'Sta112', '4', 'Sta153', '5', 'Sta125', '3', 'Sta121', '4', 'Sta11', '123'], 
    '10号线':['Sta157', '5', 'Sta114', '3', 'Sta168', '5', 'Sta135', '4', 'Sta134', '4', 'Sta85', '5', 'Sta2', '5', 'Sta4', '5', 'Sta103', '5', 'Sta145', '7', 'Sta88', '3', 'Sta87', '4', 'Sta94', '4', 'Sta160', '4', 'Sta7', '5', 'Sta6', '5', 'Sta8', '5', 'Sta75', '5', 'Sta102', '62'], 
    '4号线': ['Sta84', '8',  'Sta59', '5',  'Sta19', '6',  'Sta62', '8',  'Sta165', '9', 'Sta38', '8', 'Sta58', '24'], 
    '5号线': ['Sta43', '6',  'Sta10', '4',  'Sta96', '4',  'Sta132', '4', 'Sta37', '3', 'Sta16', '4', 'Sta69', '10', 'Sta54', '26'], 
    '11号线':['Sta77', '4',  'Sta122', '5', 'Sta36', '16', 'Sta28', '3',  'Sta124', '7', 'Sta166', '3', 'Sta99', '30', 'Sta45', '10', 'Sta152', '5', 'Sta164', '5', 'Sta82', '4', 'Sta111', '4', 'Sta140', '6', 'Sta13', '4', 'Sta70', '3', 'Sta55', '4', 'Sta20', '3', 'Sta23', '3', 'Sta56', '4', 'Sta118', '4', 'Sta115', '3', 'Sta162', '6', 'Sta15', '4', 'Sta86', '3', 'Sta46', '3', 'Sta63', '3', 'Sta3', '7', 'Sta25', '4', 'Sta146', '3', 'Sta130', '3', 'Sta120', '59'], 
    '12号线':['Sta136', '7', 'Sta137', '4', 'Sta101', '5', 'Sta31', '3',  'Sta17', '5', 'Sta26', '3', 'Sta90', '9', 'Sta95', '7', 'Sta72', '4', 'Sta93', '8', 'Sta92', '9', 'Sta116', '6', 'Sta32', '4', 'Sta91', '8', 'Sta60', '3', 'Sta148', '3', 'Sta73', '72'],
}
# 1 红色  2青色  12 黄色  11 蓝色
mark = []
with open('data/a_b_diff.csv') as f:
    f = csv.reader(f)
    for row in f:
        mark.append(0)  
# print(len(mark),mark)

with open('data/a_b_diff.csv') as f:
    f = csv.reader(f)
    change_stations = {'X':[], 'T':[], 'I':[]}
    head_tail_sta = []
    middle_sta = []  #带屏蔽的十字交叉站
    sta_sta = []
    in_sta = []  # 钉子站
    print('------------processing-------------')
    for i,row in enumerate(f):
        print(f'正在分析第{i}个')
        # ['Sta63', '11号线', 'Dist1', 'Sta129', '2号线', 'Dist1', '3']
        #     0         1        2         3        4        5     6
        is_headortail_stain = True
        is_headortail_staout = True
        if i==0:
            mark[i] = 1
            continue
        if mark[i] == 1:
            continue
        # 1. 得到数据 
        stain, routein, staout, routeout, time = row[0], row[1], row[3], row[4], row[6]
        sta1, sta1_route, sta2, sta2_route = stain, routein, staout, routeout
        # 2. 判断站点与其所在线路关系
        if stain == datadict[routein][len(datadict[routein])-2] or stain == datadict[routein][0] : is_headortail_stain = True 
        else: is_headortail_stain = False 
        if staout == datadict[routeout][len(datadict[routeout])-2] or staout == datadict[routeout][0] : is_headortail_staout = True 
        else: is_headortail_staout = False 
        # print(stain, routein,'\t', is_headortail_stain,'\t',staout,  routeout,'\t', is_headortail_staout,'\t',time)
        if int(time)>9:
            break
        #3. 处理

        # 首尾相连的两条🦌线
        if is_headortail_stain==is_headortail_staout==True:
            if routein not in head_tail_sta and routeout not in head_tail_sta:
                change_stations['I'].append(f'{stain} {routein} {staout} {routeout}')
                head_tail_sta.append(routein)
                head_tail_sta.append(routeout)
                mark[i] = 1

        # 交叉路线
        elif is_headortail_stain==False and is_headortail_staout==False:
            with open('./data/a_b_diff.csv') as f2:
                f2 = csv.reader(f2)
                for j,row2 in enumerate(f2):
                    if j<i:
                        continue
                    else:
                        sta3, sta3_route, sta4, sta4_route, time2 = row2[0], row2[1], row2[3], row2[4], row2[6]
                        # 有一个相同站， 且两个别的站在另一条线相邻
                        # print(abs(datadict[sta2_route].index(sta2)),abs(datadict[sta2_route].index(sta4)))
                        
                        if sta1==sta3 and sta2_route==sta4_route and abs(datadict[sta2_route].index(sta2)-datadict[sta2_route].index(sta4))==2 :
                            # 解决十字路口, 多条线相交
                            if sta1 in middle_sta:
                                break
                            # 解决十字路口节点被旁边的点冒充
                            if f'{sta2}{sta4}' in sta_sta:
                                break
                            change_stations['X'].append(f'{sta1_route} {sta1}  {sta2_route} {sta2} {sta4}')
                            mark[j] = 1
                            middle_sta.append(sta1)
                            sta_sta.append(f'{sta2}{sta4}')
                            sta_sta.append(f'{sta4}{sta2}')
                            break
                        elif sta1==sta4 and sta2_route==sta3_route and abs(datadict[sta2_route].index(sta2)-datadict[sta2_route].index(sta3))==2 :
                            if sta1 in middle_sta:
                                break
                            if f'{sta2}{sta3}' in sta_sta:
                                break
                            change_stations['X'].append(f'{sta1_route} {sta1} {sta2_route} {sta2} {sta3}')
                            mark[j] = 1
                            middle_sta.append(sta1)
                            sta_sta.append(f'{sta2}{sta3}')
                            sta_sta.append(f'{sta3}{sta2}')
                            break
                        elif sta2==sta3 and sta1_route==sta4_route and abs(datadict[sta1_route].index(sta1)-datadict[sta1_route].index(sta4))==2 :
                            if sta2 in middle_sta:
                                break
                            if f'{sta1}{sta4}' in sta_sta:
                                break
                            change_stations['X'].append(f'{sta2_route} {sta2} {sta1_route} {sta1} {sta4}')
                            mark[j] = 1
                            middle_sta.append(sta2)
                            sta_sta.append(f'{sta1}{sta4}')
                            sta_sta.append(f'{sta4}{sta1}')
                            break
                        elif sta2==sta4 and sta1_route==sta3_route and abs(datadict[sta1_route].index(sta1)-datadict[sta1_route].index(sta3))==2 :
                            if sta2 in middle_sta:
                                break
                            if f'{sta1}{sta3}' in sta_sta:
                                break
                            change_stations['X'].append(f'{sta2_route} {sta2} {sta1_route} {sta1} {sta3}')
                            mark[j] = 1
                            middle_sta.append(sta2)
                            sta_sta.append(f'{sta1}{sta3}')
                            sta_sta.append(f'{sta3}{sta1}')
                            break
                        
        # 丁字路线1   stain为钉子
        elif is_headortail_stain==True and is_headortail_staout==False:
            if stain not in in_sta:
                sta1,sta1_route  = stain, routein
                mark[i] = 1
                in_sta.append(stain)
                change_stations['T'].append(f'{routein} {stain} {routeout} {staout}')
            # with open('./dataFolder/a_b_diff.csv') as f2:
            #     f2 = csv.reader(f2)
            #     for j,row2 in enumerate(f2):
            #         if j<i:
            #             continue
            #         if mark[j] == 1:
            #             continue
            #         else:
            #             sta2, sta2_route, sta3, sta3_route, time2 = row[0], row[1], row[3], row[4], row[6]

        elif is_headortail_stain==False and is_headortail_staout==True:
            if staout not in in_sta:
                mark[i] = 1
                in_sta.append(staout)
                change_stations['T'].append(f'{routeout} {staout} {routein} {stain}')
    print('------------over-------------')
for key in change_stations.keys():
    for i,value in enumerate(change_stations[key]):
        print(i, ' ',value)

