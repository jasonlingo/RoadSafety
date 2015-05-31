from os import walk
import csv


def getFilename(directory, filetype):
    """Get all the file names in the directory. Return a list of filename."""
    filenameList = []
    for (dirpath, dirnames, filenames) in walk(directory):
        for filename in filenames:
            if filetype in filename:
                filenameList.append(filename)

        break
    return filenameList


def outputCSV(dataSet, filename):
    """output dataSet to a csv file"""
    print dataSet
    with open(filename, 'w') as csvfile:
        csvW = csv.writer(csvfile)
        csvW.writerows(dataSet)
    csvfile.close()