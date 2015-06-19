


import csv

x = ["abc","cde","efg"]
with open(r'yourfile.csv', 'wb', newline='') as fout:
    writer = csv.writer(fout)
    for val in x: #res is a list
        writer.writerow([val])  
    fout.close()