import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from config import OUTPUT_DIRECTORY
from File.outputCSV import outputCSV



def sumDirectionTime(directions):
    """
    sum the traffic time for every Google direction, store the result in a csv file

    Args:
      (list) directions: a list of Google directions
    Return:
      (linked list) GPSPoint: return the direction with longest time
    """

    """for check csv"""
    for direction in directions:
        print "----------------"
        direction.printNode()


    csvDataset = [["Latitude", "Longitude", "Distance", "Duration"]]
    longestTime = 0
    longestDist = 0
    longestTimeIdx = 0
    longestDistIdx = 0
    for i, direction in enumerate(directions):
        title = "Direction-" + str(i+1).zfill(4) 
        csvDataset.append([title])
        totalTime = 0
        totalDist = 0
        while(direction!=None):
            totalTime += direction.duration
            totalDist += direction.distance
            csvDataset.append( [direction.lat, direction.lng, direction.distance, direction.duration] )
            direction = direction.next
        csvDataset.append( ["Total distance:", totalDist, "Total duration:", totalTime] )
        csvDataset.append([])
        if totalTime > longestTime:
            longestTime = totalTime
            longestTimeIdx = i+1
        if totalDist > longestDist:
            longestDist = totalDist
            longestDistIdx = i+1


    csvBottom = "The direction with longest duration is: Direction-" + str(longestTimeIdx)
    csvDataset.append( [csvBottom] )
    csvBottom = "The direction with longest distance is: Direction-" + str(longestDistIdx)
    csvDataset.append( [csvBottom] )

    outputCSV(csvDataset, OUTPUT_DIRECTORY+"direction.csv")

    #return the direction with longest time
    return directions[longestTimeIdx-1]