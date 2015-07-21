import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.Haversine import Haversine


def searchGPSByDistance(gpsData, startIdx, distance):
    """
    Find the GPS data according to a given starting point of a GPS list 
    and target distance.
    
    Args:
      (list) gpsData: GPS data list.
      (int) startIdx: the starting index for searching the gpsData list.
      (float) distance: in kilometer
    Return:
      (int) index: the target index of this searching
      (datetime) gpsData[index][0]: the target GPS time
    """
    # Initialize the accumulated distance to 0.
    pathDist = 0

    # Get the first GPS point
    preGPS = gpsData[startIdx]
    
    index = startIdx
    
    # Start accumulated the GPS distance from startIdx + 1.
    # If the accumulated distance is larget than the target number, 
    # return the index and GPS time.
    for gps in gpsData[startIdx+1:]:
        # Calculate the distance between two GPS points
        tempDist = Haversine(preGPS[1][0], preGPS[1][1], gps[1][0], gps[1][1])
        pathDist += tempDist
        preGPS = gps
        index += 1
        if pathDist >= distance:
            # The accumulated distance is larger than the target distance, 
            # so stop the search process.
            break

    print "Dist: " + str(pathDist)
    return index, gpsData[index][0]