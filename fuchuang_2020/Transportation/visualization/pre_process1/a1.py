import csv
headers = ['in','out','time']
rows = []
with open('dataFolder/a1.csv') as f:

    f = csv.reader(f)
    for i, row in enumerate(f):
        if i==0:
            continue
        rows.append([row[0], row[1], row[2]   ])
        rows.append([row[1], row[0], row[2]   ])



with open('dataFolder/a2.csv','w',newline='') as f2:
    f2_csv = csv.writer(f2)
    f2_csv.writerow(headers)
    f2_csv.writerows(rows)
