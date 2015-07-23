import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from config import OUTPUT_DIRECTORY
from File.outputCSV import outputCSV



def sumDirectionTime(directions):
    """
    Sum the traffic time for every Google direction, 
    and store the result in a csv file.

    Args:
      (list) directions: a list of Google directions
    Return:
      (GPSPoint) return the direction with the longest time
    """

    # For checking the data in the output csv file is correct.
    for direction in directions:
        # Print every direction on screen.
        print "----------------"
        direction.printNode()


    # Dataset for csv file
    # The titles for each column.
    csvDataset = [["Latitude", "Longitude", "Distance", "Duration"]]
    
    # Keep tracking the direction with the longest traffic time.
    # Initialize the tracking data.
    longestTime = 0
    longestDist = 0
    longestTimeIdx = 0
    longestDistIdx = 0

    for i, direction in enumerate(directions):
        title = "Direction-" + str(i + 1).zfill(4) 
        csvDataset.append([title])
        totalTime = 0
        totalDist = 0
        while(direction != None):
            # Accumulate the traffic time and distance for each direction.
            totalTime += direction.duration
            totalDist += direction.distance
            csvDataset.append( [direction.lat, direction.lng, direction.distance, direction.duration] )
            direction = direction.next
            
        # Output the total amount of traffic time and distance
        csvDataset.append( ["Total distance:", totalDist, "Total duration:", totalTime] )
        # Add one empty row for the purpose of separating different direction data.
        csvDataset.append([])
        # Update the longest traffic time and distance.
        if totalTime > longestTime:
            longestTime = totalTime
            longestTimeIdx = i + 1
        if totalDist > longestDist:
            longestDist = totalDist
            longestDistIdx = i + 1

    # In the last part of the csv file, output the information about the direction.
    # with the longest traffic time and distance
    csvBottom = "The direction with longest duration is: Direction-" + str(longestTimeIdx)
    csvDataset.append( [csvBottom] )
    csvBottom = "The direction with longest distance is: Direction-" + str(longestDistIdx)
    csvDataset.append( [csvBottom] )
   
    # Output data to a csv file.
    outputCSV(csvDataset, OUTPUT_DIRECTORY + "direction.csv")

    # Return the direction with the longest traffic time.
    return directions[longestTimeIdx - 1]


