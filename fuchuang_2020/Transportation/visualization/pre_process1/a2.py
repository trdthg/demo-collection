import csv
headers = ['in','inroute','indist','out','outroute', 'outdist', 'time']
rows = []
with open('dataFolder/a_b_all.csv') as f:

    f = csv.reader(f)
    for i, row in enumerate(f):
        if i==0:
            continue
        rows.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
        rows.append([row[3], row[4], row[5], row[0], row[1], row[2], row[6]])



with open('dataFolder/a3.csv','w',newline='') as f2:
    f2_csv = csv.writer(f2)
    f2_csv.writerow(headers)
    f2_csv.writerows(rows)