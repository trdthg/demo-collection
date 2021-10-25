import csv
with open('data/station.csv') as f:
            f = csv.reader(f)
            namelist = []
            for row in f:
                print(row)
                # ['编号', '站点名称', '线路', '行政区域']
                if row[4] == '1':
                    namelist.append(row[1])
print(namelist)