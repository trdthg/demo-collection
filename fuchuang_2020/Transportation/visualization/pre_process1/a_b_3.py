import csv
headers = ['arrival','Stain', 'distin','departure','Staout', 'distout','time']
rows = []
with open('dataFolder/a_b_2.csv') as f1:
    f1_csv = csv.reader(f1)
    for row1 in f1_csv:
        if row1[1] == row1[4]:
            rows.append(row1)

            
with open('dataFolder/a_b_same.csv','w',newline='') as f3:
    f3_csv = csv.writer(f3)
    f3_csv.writerow(headers)
    f3_csv.writerows(rows)
