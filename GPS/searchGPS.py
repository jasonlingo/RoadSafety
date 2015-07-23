import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import datetime
import operator
from GPS.Haversine import Haversine


def searchGPSByTime(gpsData, time):
    """
    Find the index of the nearest GPS record according to the given time.

    Args:
      (list) gpsData: list of GPS data.
      (datetime) time: the time for this function to find the nearest GPS
                       record in the gpsData.
    Return:
      (int) return the index of the found GPS data in the list.
    """    

    if len(gpsData) == 0:
        # No data for this function to find
        return None
    
    # The "time" is larger than the last item, which has the largest time, 
    # in the gpsData, so return the last index of gpsData
    if time > gpsData[-1][0]:
        return len(gpsData) -1

    # The "time" is smaller than the first item, which has the smallest time, 
    # in the gpsData, so return the first index of gpsData    
    if time < gpsData[0][0]:
        return 0

    # Initialize the start and end indices of this GPS data set.
    start = 0
    end = len(gpsData)

    # Because the GPS data is recorded every 5 seconds, set the time 
    # difference to 5 seconds. 
    # If the difference between the search and target time is less than 
    # the time difference, then we found the GPS record we want.
    diff = datetime.timedelta(0,5) # 5 seconds
    
    # Using binary search
    mid = start + (end - start) / 2
    while abs(gpsData[mid][0] - time) > diff:
        if time > gpsData[mid][0]:
            start = mid + 1
        else:
            end = mid - 1
        mid = start + (end - start) / 2
    
    # Check which of gpsData[mid-1][0], gpsData[mid][0] and gpsData[mid+1][0] is 
    # the nearest time to the target time.
    compareTime = {}
    compareTime[mid] = abs(gpsData[mid][0] - time)

    if mid != len(gpsData) -1:
        compareTime[mid + 1] = abs(gpsData[mid + 1][0] - time)

    if mid > 0:
        compareTime[mid - 1] = abs(gpsData[mid - 1][0] - time)

    # Sort compareTime by value from small to large.
    SortCompareTime = sorted(compareTime.items(), key=operator.itemgetter(1))
    
    # Return the first pair's key, which is the closest index regarding to the target time
    return SortCompareTime[0][0]



def searchGPSByDistance(gpsData, startIdx, distance):
    """
    Search the GPS data that has the distance close to the target distance
    from the given starting point.
    
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
    
    # Start accumulated the GPS distance from startIdx + 1.
    # If the accumulated distance is larget than the target number, 
    # return the index and GPS time.
    index = startIdx
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


