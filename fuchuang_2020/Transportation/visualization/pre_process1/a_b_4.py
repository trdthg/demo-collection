import csv
# headers = ['arrival','Stain','departure','Staout','time']
rows = []
with open('dataFolder/station.csv') as f1:
    f1_csv = csv.reader(f1)
    for row1 in f1_csv:
        rows.append(row1[1])
        print(row1[1])
print(len(rows),len(( set(rows))))