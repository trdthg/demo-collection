import csv

with open('./data/station.csv') as f:
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
print(routes)