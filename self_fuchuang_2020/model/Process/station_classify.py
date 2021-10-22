import copy

from numpy import array, zeros, argmin, inf, equal, ndim
from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import manhattan_distances
from sklearn.cluster import KMeans, DBSCAN, k_means
import numpy as np
import matplotlib.pyplot as plt
import pymysql

class DB():
    
    def __init__(self, library="library_flow"):
        super().__init__()
        self.connect(library)

    def connect(self,DB):
        DB_USER = 'maker0'
        DB_PASS = 'Maker0000'
        DB_HOST = 'rm-bp11labi01950io698o.mysql.rds.aliyuncs.com'
        DB_PORT = 3306
        DATABASE = DB
        try:
            self.connect_info = pymysql.connect(user=DB_USER, passwd=DB_PASS, host=DB_HOST, port=DB_PORT, db=DATABASE)  #1
            self.cursor = self.connect_info.cursor()
        except:
            print("连接失败")
        
    def close(self):
        self.connect_info.close()

def dtw(a, b):
    s1 = array(a)
    s2 = array(b)
    r, c = len(s1), len(s2)
    D0 = zeros((r+1,c+1))
    D0[0,1:] = inf
    D0[1:,0] = inf
    D1 = D0[1:,1:]
    for i in range(r):
        for j in range(c):
            D1[i,j] = manhattan_distances(s1[i].reshape(-1,1),s2[j].reshape(-1,1))
    M = D1.copy()
    for i in range(r):
        for j in range(c):
            D1[i,j] += min(D0[i,j],D0[i,j+1],D0[i+1,j])
    i,j = array(D0.shape) - 2
    p,q = [i],[j]
    while(i>0 or j>0):
        tb = argmin((D0[i,j],D0[i,j+1],D0[i+1,j])) # argmin 返回index,看是哪个位置
        if tb==0 :
            i-=1
            j-=1
        elif tb==1 :
            i-=1
        else:
            j-=1
            p.insert(0,i)
            q.insert(0,j)
    return D1[-1,-1]


# DBSCAN(metric='')
def getData():
    db = DB()
    new_dict = {}
    for hour in range(6,23):
        for minute in [0,30]:
            time = f'{hour}:{minute}'
            new_dict[time] = 0
    d = []
    for key in [65.0, 49.0, 149.0, 74.0, 128.0, 34.0, 106.0, 110.0, 97.0, 80.0, 89.0, 64.0, 150.0, 154.0, 107.0, 83.0, 108.0, 47.0, 159.0, 1.0, 63.0, 129.0, 9.0, 163.0, 53.0, 79.0, 18.0, 123.0, 127.0, 81.0, 27.0, 48.0, 151.0, 68.0, 52.0, 76.0, 57.0, 71.0, 139.0, 105.0, 51.0, 24.0, 143.0, 156.0, 61.0, 50.0, 119.0, 66.0, 12.0, 161.0, 21.0, 133.0, 22.0, 138.0, 41.0, 30.0, 67.0, 144.0, 29.0, 126.0, 115.0, 40.0, 131.0, 39.0, 100.0, 135.0, 167.0, 113.0, 141.0, 142.0, 158.0, 44.0, 117.0, 147.0, 42.0, 35.0, 87.0, 109.0, 33.0, 112.0, 153.0, 125.0, 121.0, 11.0, 157.0, 114.0, 168.0, 134.0, 85.0, 2.0, 4.0, 103.0, 145.0, 88.0, 94.0, 160.0, 7.0, 6.0, 8.0, 75.0, 102.0, 90.0, 84.0, 59.0, 19.0, 62.0, 165.0, 38.0, 58.0, 43.0, 10.0, 96.0, 132.0, 37.0, 16.0, 69.0, 54.0, 56.0, 45.0, 152.0, 164.0, 82.0, 111.0, 140.0, 13.0, 70.0, 55.0, 20.0, 23.0, 118.0, 162.0, 15.0, 86.0, 46.0, 3.0, 25.0, 146.0, 130.0, 120.0, 77.0, 122.0, 36.0, 28.0, 124.0, 166.0, 99.0, 136.0, 137.0, 101.0, 31.0, 17.0, 26.0, 95.0, 72.0, 93.0, 92.0, 116.0, 32.0, 91.0, 60.0, 148.0, 73.0]:
        station = f'Sta{int(key)}'
        c = [0 for i in range(34)]
        for day in range(1,30):
            sql = f'SELECT in_flow, time_start FROM list1_3 WHERE station="{station}" and time_start REGEXP "^{day}:.+:.+" ORDER BY time_start '
            db.cursor.execute(sql)
            a = db.cursor.fetchall()
            b = copy.deepcopy(new_dict)
            for time in a:
                ttt = f"{time[1].split(':')[1]}:{time[1].split(':')[2]}"
                b[ttt] += time[0]
            b = list(b.values())
            for i in range(34):
                c[i] += b[i]
        d.append(c)
    print(len(d))
    return d


def kMeansInitCentroids(X,K):
    m = X.shape[0]
    m_arr = np.arange(0,m)      # 生成0-m-1
    centroids = np.zeros((K,X.shape[1]))
    np.random.shuffle(m_arr)    # 打乱m_arr顺序   
    rand_indices = m_arr[:K]    # 取前K个
    centroids = X[rand_indices,:]
    print('centroids', centroids.shape)
    return centroids

def findClosestCentroids(x,inital_centroids):
    m = x.shape[0]   #样本的个数
    k = inital_centroids.shape[0]  #类别的数目
    dis = np.zeros((m,k))   # 存储每个点到k个类的距离
    idx = np.zeros((m,1))   # 要返回的每条数据属于哪个类别
     
    """计算每个点到每个类的中心的距离"""
    for i in range(m):
        for j in range(k):
            dis[i,j] = dtw(x[i], inital_centroids[j])

    dummy,idx = np.where(dis == np.min(dis,axis=1).reshape(-1,1))
    return idx[0:dis.shape[0]]  

def computerCentroids(x,idx,k):
    n = x.shape[1]   #每个样本的维度
    centroids = np.zeros((k,n))   #定义每个中心点的形状，其中维度和每个样本的维度一样
    for i in range(k):
        # 索引要是一维的, axis=0为每一列，idx==i一次找出属于哪一类的，然后计算均值
        centroids[i,:] = np.mean(x[np.ravel(idx==i),:],axis=0).reshape(1,-1)
    return centroids

def runKMeans(x,initial_centroids,max_iters,plot_process):
    m,n = x.shape    #样本的个数和维度
    k = initial_centroids.shape[0]   #聚类的类数
    centroids = initial_centroids   #记录当前类别的中心
    previous_centroids = centroids   #记录上一次类别的中心
    idx = np.zeros((m,1))    #每条数据属于哪个类
    for i in range(max_iters):
        print("迭代计算次数：%d"%(i+1))
        idx = findClosestCentroids(x,centroids)
        centroids = computerCentroids(x,idx,k)   #重新计算类中心
    return centroids,idx   #返回聚类中心和数据属于哪个类别

def main():
    # data = [[1,2,3],[2,3,4],[3,4,5],[4,5,6]]
    data = getData()
    max_ = np.max(data)

    data = data / max_
    # print("聚类过程展示....\n")
    X =np.array(data).astype(np.float32)
    K = 5
    initial_centroids = kMeansInitCentroids(X,K)
    max_iters = 1
    labels = runKMeans(X,initial_centroids,max_iters,False)
    print(len(labels))
    # one_hot = [[0,0,0,0,0] for i in range(len(labels))]
    # for i in labels:
    #     one_hot[i][labels] = 1
    # return one_hot
    return labels

if __name__ == "__main__":
    a = main()
    print(a)