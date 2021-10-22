import time
import csv
headers = ['arrival','departure','time']
rows = []
i = 0
with open('dataFolder/trips.csv') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        if i==0:
            i += 1
            continue
        if row[1]==row[3]:
            continue
        intime = row[2]
        outtime = row[4]
        intime = int(time.mktime(time.strptime(row[2],'%Y/%m/%d %H:%M')))
        outtime = int(time.mktime(time.strptime(row[4],'%Y/%m/%d %H:%M')))

        dettime = outtime-intime
        # print(dettime)
        # # if outtime[0]<=2
        
        # if dettime<0:
            # print (dettime)
        rows.append([f'{row[1]}',f'{row[3]}',dettime/60.0, f'{row[2]}{row[4]}'])
        # # print (outtime)
with open('dataFolder/a_b_0.csv','w',newline='') as f2:
    f2_csv = csv.writer(f2)
    f2_csv.writerow(headers)
    f2_csv.writerows(rows)