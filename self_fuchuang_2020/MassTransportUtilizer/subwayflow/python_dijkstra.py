import csv
# from pyasn1.type.univ import None
import sys
sys.setrecursionlimit(15000)
def main(stain='Sta65', staout='Sta20'):
    # readFile = ReadFile()
    # readFile.readTxt()

    digkstra = Dijkstra(stain, staout)
    return digkstra.result()
    

class Station():

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False 
    def __hash__(self):
        return hash((self.name,))
    # order储存的是能通向该站的站
    ordermap = {}
    name = None
    linename = None
    prestation = None
    nextstation = None
    def __init__(self, name, linename=None, prestation=None, nextstation=None):
        self.name = name
        self.linename = linename
        self.prestation = prestation
        self.nextstation = nextstation

    def getNearStations(self, station):
        '''获取相邻站'''
        nearstations = []
        allstations = ReadFile.readTxt('Subway2/1.txt')
        for route in allstations:
            if station in route:
                s = route[route.index(station)]
                if s.prestation:
                    nearstations.append(s.prestation)
                if s.nextstation:
                    nearstations.append(s.nextstation)
        return nearstations

    # 传入一个sta, 把它作为键添加到ordermap中, 值为包含self的集合
    def getPasses(self, station):
        try:
            if self.ordermap[station]:
                return self.ordermap[station]
        except:
            # stalist = set()
            # stalist.add(self)
            stalist = [self,]
            self.ordermap[station] = stalist
            # stalist.add(self)
            return self.ordermap[station]
        
class ReadFile:

    number_of_allstations = 0
    
    def __init__(self):
        with open('1.txt', 'r',encoding='utf-8') as f:
            f = f.readlines()
            for line in f:
                line = line[:].split(' ')
                self.number_of_allstations += len(line)

        # print(self.number_of_allstations)

    # @staticmethod
    def readTxt(self, filepath = '1.txt'):
        a = []
        presta = None
        with open(filepath, 'r',encoding='utf-8') as f:
            f = f.readlines()
            for line in f:
                b = []
                line = line[:].split(' ')
                for i in range(1, len(line)):
                    sta = Station(line[i],line[0])
                    b.append(sta)
                    # print(sta.name)
                    # number_of_allstations += 1
                    if i!=1:
                        sta.prestation = presta
                        presta.nextstation = sta
                    presta = sta
                a.append(b)
        return a
    
    def readCsv(self,filepath=None):
        with open(filepath, 'r', encoding='utf-8') as f:
            f = csv.reader(f)
            return f

class Dijkstra:
    '''计算路径'''
    # nearestpass = []
    # stain = None
    # staout = None

    def __init__(self, stain='Sta65', staout='Sta128'): 
        # 初始化 stain staout
        flag = 0
        self.readFile = ReadFile()
        a = self.readFile.readTxt()
        for route in a:
            for sta in route:
                if sta.name == stain:
                    self.stain = sta
                    
                if sta.name == staout:
                    self.staout = sta
        # 初始化 stain的ordermap
        for sta in self.stain.getNearStations(self.stain):
            self.stain.getPasses(sta).append(sta)
        # print('初始化', self.stain, self.staout)
        # 添加stain到pass中
        self.nearestpass= [self.stain]
    
    def getShorterPath(self, station):
        '''获取更近的站点'''
        a = 10000
        neareststa = None
        for sta in station.ordermap.keys():
            if sta in self.nearestpass: 
                 continue
            newpass = station.getPasses(sta)
            if len(newpass) < a :
                a = len(newpass)
                neareststa = sta
        return neareststa

    def result(self):
        '''nb'''
        # 初始化
        # print(len(self.nearestpass))
        nearstation = self.getShorterPath(self.stain)
        if len(self.nearestpass) == self.readFile.number_of_allstations:
            print('第一处判定位置')
            sortedlist = sorted(set(self.stain.getPasses(self.staout)), key=self.stain.getPasses(self.staout).index)
            namelist = []
            for i,sta in enumerate(sortedlist):
                namelist.append(sta.name)
            return namelist

        if nearstation == self.staout:
            linename = ''
            # print('第二处判定位置')
            # print(f'起点: {self.stain.name} 终点站: {self.staout.name}')
            sortedlist = sorted(set(self.stain.getPasses(self.staout)), key=self.stain.getPasses(self.staout).index)
            namelist = []
            for i,sta in enumerate(sortedlist):
                namelist.append(sta.name)
                # if sta==self.staout:
                #     print(sta.name,sta.linename)
                #     pass
                # else:
                #     if sta.linename != linename and i!=0:
                #         print()
                #     print(sta.name,sta.linename, ' -> ', end='')
                # linename = sta.linename
            # print(namelist)
            return namelist
        for near2station in self.stain.getNearStations(nearstation):

            if near2station in self.nearestpass:
                continue
            length_of_pass = len(self.stain.getPasses(nearstation))
            if near2station in self.stain.getPasses(near2station):

                if len(self.stain.getPasses(near2station))-1 > length_of_pass:
                    # self.stain.getPasses(near2station).clear()
                    # self.stain.getPasses(near2station)
                    # print(self.stain.getPasses(near2station).append)
                    self.stain.getPasses(near2station).extend(self.stain.getPasses(nearstation))
                    self.stain.getPasses(near2station).append(near2station)
                else:
                    pass
            else:
                self.stain.getPasses(near2station).extend(self.stain.getPasses(nearstation))
                self.stain.getPasses(near2station).append(near2station)
        
        self.nearestpass.append(nearstation)
        # print(len(self.stain.getPasses(nearstation)))
        return self.result()

if __name__ == '__main__':
    main()


