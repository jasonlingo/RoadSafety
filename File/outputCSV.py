import csv

def outputCSV(dataSet, filename):
    """output dataSet to a csv file"""
    
    with open(filename, 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in dataSet:
            writer.writerow(val)   
    output.close()