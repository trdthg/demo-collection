import csv

'''
$判断是否出现过相同站点:
    1.若两战点均出现过:跳过

    2.若只有一个出现  :
        若出现的无子节点: 添加节点

        若出现的有子节点: 
            暂时只考虑第一种情况
            1)若有一个子结点:
                判断两个子节点到同一节点的时间
            2)若有多个子节点:        
                这种情况应该不会发生, 因为时间段的节点一般都已经出现了
                艹我炸了, 应该不用管, 毕竟有时间限制
    3.若两个都未出现过:
        暂时选择第一种方案
        1) 滞后处理
        2) 没法办
'''
station_dict = {}
stain = ''
staout = ''
flag = [0,0]   # 标记两个站点的存在状态
is_over = 0
another_child_key = 0

def dict_ergodic(father_dict):
    global flag
    # -----标记遍历这个嵌套字典-----
    for key in father_dict.keys():  #处理措施放这里
        # print(key)
        child_dict = father_dict[key]
        if flag==[1,1]:
            break
        if key==stain:
            flag[0] = 1
        if key==staout:
            flag[1] = 1
        if child_dict == {}:
            continue                   # 到达尽头
        else:
            dict_ergodic(child_dict)  # 深入到下一层

def dict_ergodic_in(father_dict):
    # -----遍历这个嵌套字典-----
    global another_child_key
    global is_over
    for key in father_dict.keys():  #处理措施放这里
        if is_over==1:
            break
        if key==stain:
            child_dict = father_dict[key]
            # 无子节点
            if child_dict == {}:
                over = 1
                child_dict[staout] = {}
                break
            # 有子节点, 记下他的名字
            else:
                for key in child_dict.keys():
                    another_child_key = key
                    break
                child_dict[staout] = {}
                break

        child_dict = father_dict[key]
        
        if child_dict == {}:
            continue                   # 到达尽头
        else:
            dict_ergodic(child_dict)  # 深入到下一层

with open('./data/a_b_same.csv') as f:
    f = csv.reader(f)
    i = 0
    for row in f:
        if i==0:
            i+=1
            continue
        if i==1:
            i+=1
            station_dict[row[0]] = {row[3]: {}}
            continue
        # ['Sta64', '1号线', 'Dist3', 'Sta150', '1号线', 'Dist3', '3']
        stain, staout = row[0], row[3]
        # 标记
        dict_ergodic(station_dict)
        # 实战
        if flag==[1,1]:
            pass
        elif flag==[1,0]:
            # 找到两个子节点
            dict_ergodic_in(station_dict)
            # 判断谁在前

            # with open('./dataFolder/a_b_same.csv') as f2:
            #     f2 = csv.reader(f2)
            #     compile_time = {}
            #     for row in f2:
            #         if row[0] == stain and row[3] != another_child_key :
            #             compile_time[row[3]] = [row[0], ,
            #             pass
            
        elif flag==[0,1]:
            # dict_ergodic_out(station_dict)
            pass
        elif flag==[1,1]:
            pass
        # 重制标记
        flag = [0,0]
        is_over = 0
        another_child_key = 0

        i += 1

print(station_dict)