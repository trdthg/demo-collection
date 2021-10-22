import xlrd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import multiprocessing as mp
import asyncio
routes_stations = {}
def main():
    print('正在获取文件')
    book_station = xlrd.open_workbook('dataFolder/station.xlsx')
    book_trips = xlrd.open_workbook('dataFolder/trips.xlsx')
    print('正在获取表格')
    sheet_station = book_station.sheets()[0]
    sheet_trips = book_trips.sheets()[0]
    print('正在解析表格')
    col_datalist_station_station = sheet_station.col_values(1,start_rowx=1,end_rowx=None)
    col_datalist_station_route = sheet_station.col_values(2,start_rowx=1,end_rowx=None)
    col_datalist_trips_arrival = sheet_trips.col_values(3,start_rowx=3,end_rowx=None)

    # allstations = mp.Manager().dict()
    allstations = {}

    # routes_stations = {}
    # allstations = set()
    print('开始统计')
    getdatalist(routes_stations, col_datalist_station_route, col_datalist_station_station, allstations)

    lock = mp.Lock()
    
    print (allstations)
    # 1-多核方法
    # print('多核遍历中')
    # pool = mp.Pool(16)
    # i = 0
    # for arrival in col_datalist_trips_arrival:
    #     i += 1
    #     print(i)
    #     pool.apply(gettrip, (arrival, allstations))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    # pool.close()
    # pool.join()   #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    # print ("Sub-process(es) done.")

    # 2-原本方法
    i = 0
    for arrival in col_datalist_trips_arrival:
        i += 1
        print(i)
        # print(allstations)
        if arrival in allstations.keys():
            allstations[arrival] += 1
    print('统计完成')

    # 3-异步方法
    # loop = asyncio.get_event_loop()
    # i = 0
    # for arrival in col_datalist_trips_arrival:
    #     i += 1
    #     print(i)
    #     loop.run_until_complete(gettrip(arrival,allstations))

    # 4-map方法 失败
    # pool = mp.Process(16)
    # pool.map(gettrip, col_datalist_trips_arrival)
    def gettrip(arrival):
        # allstations
        # print(arrival)
        # lock.acquire()
        if arrival in allstations.keys():
            allstations[arrival] += 1
        # lock.release()

    print (allstations)

    drawpicture_one(allstations)
    # drawpicture_many(lines)
    
    

    
def getstations(router,col_datalist_station_station,col_datalist_station_route, allstations):
    # global allstations
    for station, route in zip(col_datalist_station_station,col_datalist_station_route):
        routes_stations[route].add(station)
        if station not in allstations.keys():
            
            allstations[station] = 0
            # print(allstations[station])

def getdatalist(routes_stations, col_datalist_station_route, col_datalist_station_station, allstations):
    # global allstations
    for route in set(col_datalist_station_route):
        routes_stations[route] = set()
    print('得到了所有的线路')
    print(routes_stations.keys())
    for route in routes_stations.keys():
        print(f'正在获取{route}的车站')
        getstations(route,col_datalist_station_station,col_datalist_station_route, allstations)
        print(routes_stations[route])


def drawpicture_many(lines):
        # 单图展示
        for line in lines:
            plt.figure()
            n = len(line)
            x = line.keys()
            y = line.values()
            ax = plt.gca()
            for label in ax.get_xticklabels():
                label.set_fontsize(10)
            plt.plot(x,y)
            # break
        print('开始绘图')
        plt.show()

def drawpicture_one(allstations):
        print('正在构建坐标系')
        fig = plt.figure(figsize=(20,40))
        # fig.set_figheight(300)
        # fig.set_figwidth(100)
        i=0
        k=0
        j=0
        print(routes_stations['4号线'])
        for route in routes_stations.keys():
            ax = plt.subplot2grid( (int(len(routes_stations.keys())/2) , 2), (i,k), rowspan=1, colspan=1)
            x = list(routes_stations[route])  # x为关于线路上站点的列表
            x1 = [lll.split('a')[1] for lll in x]
            y = []
            for station in x:
                if station in allstations.keys():
                    y.append(allstations[station])
                else:
                    y.append(0)
            ax.plot(x1, y)
            ax.set_title(route, fontproperties="FangSong")
            j += 1
            i += 1
            if k==0: 
                k=1
                i-=1
            else: k=0
        plt.tight_layout(w_pad=4, h_pad=12)
        # plt.subplots_adjust(hspace =20)#调整子图间距
        print('开始绘图')
        plt.show()

if __name__ == '__main__':
    main()

