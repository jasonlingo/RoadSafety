import csv

def outputCSV(dataSet, filename):
    """
    Output dataSet to a csv file

    Args:
      (list) dataSet: the data set to be written to a csv file
      (String) filename: the output csv file name
    """
    
    with open(filename, 'w') as output: # Open a csv file
        writer = csv.writer(output, lineterminator='\n')
        
        # Write data to a csv file one record a line
        for val in dataSet:
            writer.writerow(val)   
    output.close()