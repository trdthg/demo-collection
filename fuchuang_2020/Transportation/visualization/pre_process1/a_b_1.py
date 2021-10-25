import csv
headers = ['arrival','Stain','departure','Staout','time']
rows = []
stations_name = {}
arr = []
i = 0
with open('dataFolder/a_b_0.csv') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        # print(i)
        if i==0:
            i += 1
            continue
        if f'{row[0]}{row[1]}' in arr:
            continue
        if row[0] == row[1]:
            print('sss')
            continue
        # print(i)

        i+=1
        rows.append([f'{row[0]}', f'{row[1]}', f'{row[2]}'])
        # rows.append(f'{row[1]}', f'{row[0]}', f'{row[2]}')
        arr.append(f'{row[0]}{row[1]}')
        arr.append(f'{row[1]}{row[0]}')
#         row[2] = int(row[2])
#         if f'{row[1]}{row[0]}' in stations_name.keys():
#             if rows[stations_name[f'{row[1]}{row[0]}']][4] > row[2]:
#                 rows[stations_name[f'{row[1]}{row[0]}']][4] = row[2]
#             continue
#         if f'{row[0]}{row[1]}' in stations_name.keys():
#             if rows[stations_name[f'{row[0]}{row[1]}']][4] > row[2]:
#                 rows[stations_name[f'{row[0]}{row[1]}']][4] = row[2]
#             continue
#         stations_name[f'{row[0]}{row[1]}']=i-1
#         rows.append([f'{row[0]}','',f'{row[1]}','',row[2]])
#         i+=1
#         # if int(row[2])<10:
#             # print(row[2])
# # print(stations_name)
with open('dataFolder/a2.csv','w',newline='') as f2:
    f2_csv = csv.writer(f2)
    f2_csv.writerow(headers)
    f2_csv.writerows(rows)