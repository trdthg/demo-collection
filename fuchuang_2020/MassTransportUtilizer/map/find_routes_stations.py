import csv

def getstations():
    # ['编号', '站点名称', '线路', '行政区域']
    with open('./dataFolder/station.csv') as f:
        f = csv.reader(f)
        routes = {}
        i = 0
        for row in f:
            if i==0:
                i+=1
                continue
            if row[2] not in routes.keys():
                routes[row[2]] = []
            if row[1] not in routes[row[2]]:
                routes[row[2]].append(row[1])
    return routes

def jjj(j, arr, route):

    flag = 0
    if j >= len(stationdatalist[route])*2-2:
        pass
    else:
        time2 = ''
        time1 = ''
        sta1 = ''
        sta2 = ''
        with open('./dataFolder/a_b_same.csv') as f1:
            f1 = csv.reader(f1)
            for row_ in f1:
                if row_[1]==route and row_[4]==route:
                    stain, staout, time = row_[0], row_[3], row_[6]
                    if arr[j] == stain:
                        if staout not in arr:
                            time1 = time
                            sta1 = staout
                            j += 2
                            flag = 1
                            break
                    if arr[j] == staout:
                        if stain not in arr:
                            time1 = time
                            sta1 = stain
                            j += 2
                            flag = 1
                            break
        with open('./dataFolder/a_b_same.csv') as f1:
            f1 = csv.reader(f1)
            for row__ in f1:
                if row__[1]==route and row__[4]==route:
                    stain, staout, time = row__[0], row__[3], row__[6]
                    if arr[0] == stain:
                        if staout not in arr:
                            time2 = time
                            sta2 = staout
                            j += 2
                            flag = 1
                            break
                    if arr[0] == staout:
                        if stain not in arr:
                            time2 = time
                            sta2 = stain
                            j += 2
                            flag = 1
                            break
        if time2 != '' and time1 != '':
            j-=2
            if int(time1) >= int(time2):
                arr.insert(0, time2)
                arr.insert(0, sta2)
            else:
                arr.append(time1)
                arr.append(sta1)
        if time2 == '' and time1 !='':
            arr.append(time1)
            arr.append(sta1)
        if time1 == '' and time2 !='':
            arr.insert(0, time2)
            arr.insert(0, sta2)
        jjj(j, arr, route)

def main():
    
    for route in getstations().keys():
        with open('./dataFolder/a_b_same.csv') as f:
            f = csv.reader(f)
            i = 0
            arr = [0,0,0]
            for row in f:
                if i==0:
                    i+=1
                    continue
                if row[1]==route and row[4]==route:
                    i+=1
                    arr[0] = row[0]
                    arr[1] = row[6]
                    arr[2] = row[3]
                    # print (arr)
                    jjj(2, arr, route)
                    break
                # ['Sta64', '1号线', 'Dist3', 'Sta150', '1号线', 'Dist3', '3']
                i+=1
        # print(arr[-1])
        with open('./dataFolder/a_b_same.csv') as f:
            f = csv.reader(f)
            for row in f:
                if (row[0]==arr[-1] and row[3]==arr[0]) or (row[0]==arr[0] and row[3]==arr[-1]):
                    arr.append(row[6])
                    break
        stationdatalist[route] = arr
        print (route,arr)
        # break
    # print(stationdatalist)

stationdatalist = getstations()

if __name__ == '__main__':
    main()
# 5号线 ['Sta43', '6', 'Sta10', '4', 'Sta96', '4', 'Sta132', '4', 'Sta37', '3', 'Sta16', '4', 'Sta69', '10', 'Sta54', '26']