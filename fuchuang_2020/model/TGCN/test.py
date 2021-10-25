import pandas as pd
# s1 = pd.read_csv('./data/1.csv', header=None)
# sz_adj = pd.read_csv('./data/sz_adj.csv', header=None)
# sz_speed = pd.read_csv('./data/sz_speed.csv', header=None)
# print(s1.shape)
# print(sz_adj.shape)
# print(sz_speed.shape)
'''
SZ-taxi。该数据集由深圳2015年1月1日至1月31日的出租车轨迹数据组成，
本文选取罗湖区156条主要道路作为研究区域。实验数据主要包括两部分。

一个是156*156的邻接矩阵，它描述了道路之间的空间关系。
每一行表示一条道路，矩阵中的值表示道路之间的连接性。

另一个是特征矩阵，它描述了每条道路上的速度随时间的变化。
每一行代表一条路，每一列是不同时段道路上的交通速度。我们每15分钟计算一次每条路上的车速。'''


# 每组数据间以 (5, 10, 15) 分钟为间隔的话

# 一个小时内精确估计
# 输入数据   12组 进展流量, 线路断面流量
# 输出数据   3组  出战流量, 线路断面流量

# 超过1个小时只能粗略估计

a = pd.DataFrame(pd.read_csv('./test.csv', header=None))
def b(a):
    return a[1]
c = a.apply(b, axis=1)
print(c)
