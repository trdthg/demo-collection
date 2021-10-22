sdict = {'origin':{
            'before':{
                'a11':{
                    'a111':{
                    },
                    },
                'a12':{
                    'a121':{
                        'a1211':{
                        },
                        },
                        },
                        },
            'after':{
                'b11':{
                    'b21':{
                    },
                    },
                    },
                    },
        'sss':{}}
def sss(child_dict):
    for key in child_dict.keys():
        print(key)
        child_dict_ = child_dict[key]
        if child_dict_ == {}:
            # 到达尽头
            continue
        else:
            # 深入到下一层
            sss(child_dict_)
# for key in sdict.keys():
#     print (key)
#     child_dict = sdict[key]
#     # 子字典自我遍历
#     for key in child_dict.keys():
#         print(key)
#         child_dict_ = child_dict[key]
#         if child_dict_ == {}:
#             # 到达尽头
#             continue
#         else:
#             # 深入到下一层
#             sss(child_dict_)
# flag = 0
sss(sdict)
p = ['lll','kkk','iiii','ooo']
# print(p.index('kkk'))
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
b = []
for key in datadict.keys():
    for i,val in enumerate(datadict[key]):
        # print(i)
        flag = 0
        with open('./dataFolder/station.csv') as f:
            f = csv.reader(f)
            for row in f:
                if val == row[1]:
                    b.append(row[3])
                    flag = 1
                    break
        if flag == 0:
            b.append(0)
        # print('---over---')
    print(key + ': ' + f'{b}')
    print()
    b = []