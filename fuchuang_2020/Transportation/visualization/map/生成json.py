'''
stations[
	{
		id: id,
		x: x,
		y: y,
		level: level,
		type: type,
		line: line,
		station: station
	},
	…
]
id 用于识别的标识符
x 站点在地图上的横坐标（相对）
y 站点在地图上的纵坐标（相对）
level 站点的等级，会以大小/热力形式显示
type 站点类型（没想好
line 线路 
station 站名
'''
routes = {
    '1号线': ['Sta65', 'Sta49', 'Sta149', 'Sta74', 'Sta128', 'Sta34', 'Sta106', 'Sta110', 'Sta97', 'Sta80', 'Sta89', 'Sta64', 'Sta150', 'Sta154', 'Sta107', 'Sta83', 'Sta108', 'Sta159', 'Sta1'], 
    '2号线': ['Sta129', 'Sta9', 'Sta163', 'Sta53', 'Sta79', 'Sta18', 'Sta47', 'Sta123', 'Sta127', 'Sta81', 'Sta27', 'Sta48', 'Sta151', 'Sta68', 'Sta52', 'Sta76', 'Sta57', 'Sta71', 'Sta139', 'Sta105', 'Sta51', 'Sta24'], 
    '3号线': ['Sta143', 'Sta156', 'Sta61', 'Sta50', 'Sta119', 'Sta66', 'Sta12', 'Sta161', 'Sta21', 'Sta133', 'Sta22', 'Sta138', 'Sta41', 'Sta30', 'Sta67', 'Sta144', 'Sta29', 'Sta126', 'Sta40', 'Sta131', 'Sta39', 'Sta100', 'Sta167', 'Sta113', 'Sta141', 'Sta142', 'Sta158', 'Sta44', 'Sta117', 'Sta147', 'Sta42', 'Sta35', 'Sta109', 'Sta33', 'Sta112', 'Sta153', 'Sta125', 'Sta121', 'Sta11'], 
    '10号线': ['Sta157', 'Sta114', 'Sta168', 'Sta135', 'Sta134', 'Sta85', 'Sta2', 'Sta4', 'Sta103', 'Sta145', 'Sta88', 'Sta87', 'Sta94', 'Sta160', 'Sta7', 'Sta6', 'Sta8', 'Sta75', 'Sta102'], 
    '4号线': ['Sta84', 'Sta59', 'Sta19', 'Sta62', 'Sta165', 'Sta38', 'Sta58'], 
    '5号线': ['Sta43', 'Sta10', 'Sta96', 'Sta132', 'Sta37', 'Sta16', 'Sta69', 'Sta54'], 
    '11号线': ['Sta77', 'Sta122', 'Sta36', 'Sta28', 'Sta124', 'Sta166', 'Sta99', 'Sta45', 'Sta152', 'Sta164', 'Sta82', 'Sta111', 'Sta140', 'Sta13', 'Sta70', 'Sta55', 'Sta20', 'Sta23', 'Sta56', 'Sta118', 'Sta115', 'Sta162', 'Sta15', 'Sta86', 'Sta46', 'Sta3','Sta63',  'Sta25', 'Sta146', 'Sta130', 'Sta120'], 
    '12号线': ['Sta136', 'Sta137', 'Sta101', 'Sta31', 'Sta17', 'Sta26', 'Sta90', 'Sta95', 'Sta72', 'Sta93', 'Sta92', 'Sta116', 'Sta32', 'Sta91', 'Sta60', 'Sta148', 'Sta73']
}
import csv
import json
import os
def write_list_to_json(list, json_file_name, json_file_save_path):
    """
    将list写入到json文件
    :param list:
    :param json_file_name: 写入的json文件名字
    :param json_file_save_path: json文件存储路径
    :return:
    """
    os.chdir(json_file_save_path)
    with open(json_file_name, 'w', encoding='utf-8') as  f:
        json.dump(list, f)

print(len(routes['2号线']))
coordinate = {
    '1号线':{
        1:[7744, 11382+527*10],
        2:[7744, 11382+527*9],
        3:[7744, 11382+527*8],
        4:[7744, 11382+527*7],
        5:[7744, 11382+527*6],
        6:[7744, 11382+527*5],
        7:[7744, 11382+527*4],
        8:[7744, 11382+527*3],
        9:[7744, 11382+527*2],
        10:[7744, 11382+527*1],
        11:[7744, 11382],
        12:[7744, 10206],
        13:[(7744+9454)/2, 10206],
        14:[9454, 10206],
        15:[9452, 4310 + 1179*4],
        16:[9452, 4310 + 1179*3],
        17:[9452, 4310 + 1179*2],
        18:[9452, 4310 + 1179*1],
        19:[9452, 4310 + 1179*0],
    },
    "2号线":{
        1:[14448-715*1, 5980],
        2:[14448-715*2, 5980],
        3:[14448-715*3, 5980],
        4:[14448-715*4, 5980],
        5:[14448-715*5, 5980],
        6:[14448-715*6, 5980],
        7:[14448-715*7, 5980],
        8:[8728, 5980],
        9:[8728, (5980+8076)/2],
        10:[8728, 8076],
        11:[166+713*11, 8076],
        12:[166+713*10, 8076],
        13:[166+713*9, 8076],
        14:[166+713*8, 8076],
        15:[166+713*7, 8076],
        16:[166+713*6, 8076],
        17:[166+713*5, 8076],
        18:[166+713*4, 8076],
        19:[166+713*3, 8076],
        20:[166+713*2, 8076],
        21:[166+713*1, 8076],
        22:[166, 8076]
    },
    '3号线': {
        1:[15196, 114],
        2: [15196, 114+796*1],
        3: [15196, 114+796*2],
        4: [15196, 114+796*3],
        5: [15196, 114+796*4],
        6: [15196, 114+796*5],
        7: [15196, 114+796*6],
        8: [15196, 114+796*7],
        9:[15196, 6480],
        10:[11078+1373*2, 6480],
        11:[11078+1373, 6480],

        12:[11078, 6480],
        13:[11078, 7024],
        14:[11078, 7024+431*1],
        15:[11078, 7024+431*2],
        16:[11078, 7024+431*3],
        17:[11078, 7024+431*4],
        18:[11078, 7024+431*5],

        19:[11704, 10012],
        20:[11704+595, 10012],
        21:[11704+595*2, 10012],
        22:[13490, 10012],
        
        23:[14762, 10012],
        24:[14762+691*1, 10012],
        25:[14762+691*2, 10012],
        26:[14762+691*3, 10012],
        27:[14762+691*4, 10012],
        28:[14762+691*5, 10012],
        29:[18908, 10012],
        30:[18908, 10012+570.5*1],
        31:[18908, 10012+570.5*2],
        32:[18908, 10012+570.5*3],
        33:[18908, 10012+570.5*5],
        34:[18908, 10012+570.5*6],
        35:[18908-738*0, 14006],
        36:[18908-738*1, 14006],
        37:[18908-738*2, 14006],
        38:[18908-738*3, 14006],
        39:[15954, 14006]
    },
    '10号线': {

        # 1: [13490, 8288],
        # 2: [13490, 8878],
        1: [13490, 10012-598*3],
        2: [13490, 10012-598*2],
        3: [13490, 10012-598],
        4: [14034, 10012],
        5: [14444, 10520],

        6: [14852, 11094],
        7: [14852+1037, 11094],
        8: [14852+1037*2, 11094],
        9: [17964, 11094],

        10: [17964, (11094+12242)/2],
        11:[17962, 12242],
        12:[(17962+19850)/2, 12242],
        13:[19850, 12242],
        14:[19850, 12242+632*1],
        15:[19850, 12242+632*2],
        16:[19850, 12242+632*3],
        17:[19850, 12242+632*4],
        18:[19850, 15320],
        19:[19860, 16032],
    },
    '4号线': {
        1:[11070+1127*2, 11876],
        2:[11070+1127*2, 12378],
        3:[11070+1127*2, 12882],
        4:[11070+1127*2+784*1, 12882],
        5:[11070+1127*2+784*2, 12882],
        6:[11070+1127*2+784*3, 12882],
        7:[11070+1127*2+784*4, 12882],
    },
    '5号线': {
        8:[11068+941, 10788],
        7:[11068+941*2, 10788],
        6:[13894, 10788],
        5:[13894, 11922],
        4:[13894+819, 11922],
        3:[13894+819*2, 11922],
        2:[13894+819*3, 11922],
        1:[17172, 11920],
    },
    '11号线': {
        1: [14172, 19300],
        2: [14172, 19300-569*1],
        3: [14172, 19300-569*2],
        4: [14172, 19300-569*3],
        5: [14172, 19300-569*4],
        6: [14172, 19300-569*5],
        7: [14172, 19300-569*6],

        8:[19852+1136*1, 15320],
        9:[19852-1136*1, 15320],
        10:[19852-1136*2, 15320],
        11:[19852-1136*3, 15320],
        12:[19852-1136*4, 15320],

        13: [14172, 15320],
        14:[13210, 14658],
        15:[12216, 13954],
        16:[11078, 13152],

        17:[11078, (13152+11360)/2],
        18:[11078, 11360],
        19:[11078, 9618+581*2],
        20:[11078, 9618+581],
        21:[11078, 9618],

        # 22:[12136, 9226],9432
        22:[11704+595, 10012-598*2],
        # 23:[14452, 8408],
        23:[14452, 10012-598*2],
        24:[14452, 10012-598*3],
        25:[14452, 10012-598*4],
        # 24:[14452, 7026+461*2],
        # 25:[14452, 7026+461*1],
        26:[14452, 7026],
        27:[14444, 5990],
        28:[14444, 5990-761*1],
        29:[14444, 5990-761*2],
        30:[14444, 5990-761*3],
        31:[14450, 2946],
    },
    '12号线': {
        1:  [7112, 11382],
        2:  [7744+665, 11382],
        3:  [7744+665*2, 11382],
        4:  [7744+665*3, 11382],
        5:  [7744+665*4, 11382],

        6:  [11070+1127*1, 11384],
        7:  [11070+1127*2, 11384],

        8:  [14450, 9312+100],
        9:  [15196, 10012-598*2.7],
        10: [15196, 10012-598*4.3],
        11:  [13656, 7024],
        12:  [12750, 7024],
        13:  [11916, 7024],
        14:  [9916, 7024],
        15:  [7682, 7024],
        16:  [6644, 7024],
        17:  [5594, 7024],

    }


}
stations = []
for route in routes.keys():
    # if route != '1号线':
    #     continue
    for i,needsta in enumerate(routes[route]):
        with open('data/station.csv') as f:
            f = csv.reader(f)
            for row in f:
                # ['编号', '站点名称', '线路', '行政区域']
                sta = row[1]
                if sta==needsta:
                    if sta in routes[route]:
                        index = routes[route].index(sta)
                        xy = coordinate[route][index+1]
                        stations.append(
                            {
                                'id':int(row[0]),
                                'x': xy[0],
                                'y': xy[1],
                                'level': '',
                                'type': row[4],
                                'line': row[2],
                                'station':row[1],
                                'dist':row[3],
                            }
                        )
                        break
for i,item in enumerate(stations) :
    print(i, ' ' ,item)


# write_list_to_json(stations, 'stations.json', './')



# paths[
# 	{
# 		id: id,
# 		x1: x1,
# 		y1: y1,
# 		x2: x2,
# 		y2: y2,
# 		level: level,
# 		line: line
# 	},
# 	…
# ]
# id 用于识别的标识符
# x1 起始点在地图上的横坐标（相对）
# y1 起始点在地图上的纵坐标（相对）
# x2 结束点在地图上的横坐标（相对）
# y2 结束点在地图上的纵坐标（相对）
# level 路径的等级，会以粗细显示
# line 线路

paths = []
middlesta_before = {
    'Stta136':'Sta89',
    'Sta108': 'Sta47',
    'Sta91':'Sta127', 
    'Sta32':'Sta41',
    'Sta126':'Sta115',
    'Sta17':'Sta23', 
    'Sta93':'Sta3',
    'Sta162':'Sta114',
    'Sta95':'Sta15',
    'Sta100':'Sta135',
    'Sta35':'Sta87',
    'Sta99': 'Sta140',
    'Sta45':'Sta75',
    'Sta90':'Sta134',

}
middlesta_after = {
    'Sta89':'Sta137',
    'Sta47':'Sta159',
    'Sta127':'Sta60',
    'Sta41':'Sta91',
    'Sta115':'Sta40',
    'Sta23':'Sta26',
    'Sta84':'Sta90',
    'Sta56':'Sta54',
    'Sta3':'Sta92',
    'Sta114':'Sta15',
    'Sta15':'Sta95',
    'Sta134':'Sta95',
   'Sta63' :'Sta129',
    'Sta15':'Sta72',

    'Sta135':'Sta167',
    'Sta87':'Sta109',
    'Sta75':'Sta152',
}
i = 0
for station in stations:
    sta = station['station']
    
    if station['station'] in middlesta_before.keys():
        for nextstation in stations:
            if nextstation['station']==middlesta_before[station['station']]:
                if station['station'] == 'Sta90':
                    paths.append({
                        's1':station['station'],
                        's2':nextstation['station'],
                        'id': i,
                        'x1': station['x'],
                        'y1': station['y'],
                        'x2': nextstation['x'],
                        'y2': nextstation['y'],
                        'leval': '',
                        'line':station['line'],
                        'additionalCoordinates': [nextstation['x'],station['y']]
                    })
                elif  station['station'] == 'Sta93':
                    paths.append({
                        'id': i,
                        's1':station['station'],
                        's2':nextstation['station'],
                        'x1': station['x'],
                        'y1': station['y'],
                        'x2': nextstation['x'],
                        'y2': nextstation['y'],
                        'leval': '',
                        'line':station['line'],
                        'additionalCoordinates': [station['x'],nextstation['y']]
                    }) 
                else:
                    paths.append({
                        'id': i,
                        's1':station['station'],
                        's2':nextstation['station'],
                        'x1': station['x'],
                        'y1': station['y'],
                        'x2': nextstation['x'],
                        'y2': nextstation['y'],
                        'leval': '',
                        'line':station['line'],
                    })
                
                i+=1
                break
        continue
    if station['station'] in middlesta_after.keys():

        for nextstation in stations:
            if nextstation['station']==middlesta_after[station['station']]:
                if station['station']== 'Sta84':
                    paths.append({
                    'id': i,
                    's1':station['station'],
                    's2':nextstation['station'],
                    'x1': station['x'],
                    'y1': station['y'],
                    'x2': nextstation['x'],
                    'y2': nextstation['y'],
                    'leval': '',
                    'line':station['line']
                })
                elif station['station']=='Sta15':
                    paths.append({
                        'id': i,
                        's1':station['station'],
                        's2':nextstation['station'],
                        'x1': station['x'],
                        'y1': station['y'],
                        'x2': nextstation['x'],
                        'y2': nextstation['y'],
                        'leval': '',
                        'line':nextstation['line'],
                        'additionalCoordinates': [nextstation['x'],station['y']]
                    })
                else:
                    paths.append({
                        's1':station['station'],
                        's2':nextstation['station'],
                        'id': i,
                        'x1': station['x'],
                        'y1': station['y'],
                        'x2': nextstation['x'],
                        'y2': nextstation['y'],
                        'leval': '',
                        'line':nextstation['line']
                    })
                
    try:
        if station['line'] != stations[i+1]['line']:
            # 这条线路结束
            i+=1
            continue 
        else:
            try:
                
                paths.append({
                    's1':station['station'],
                    's2':stations[i+1]['station'],
                    'id': i,
                    'x1': station['x'],
                    'y1': station['y'],
                    'x2': stations[i+1]['x'],
                    'y2': stations[i+1]['y'],
                    'level': '',
                    'line':station['line'],
                })
                i+=1
            except:
                pass
    except:
        i+=1
        pass
    
new_dict = {}
for item in paths:
    print(item)
    new_dict[(item['s1'], item['s2'])] = item['line']
    new_dict[(item['s2'], item['s1'])] = item['line']
print(new_dict)
    
# print(paths)
# write_list_to_json(paths, 'paths.json', './')
