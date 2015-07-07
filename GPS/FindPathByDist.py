import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.Haversine import Haversine


def FindPathByDist(gpsData, startIdx, distance):
    """
    Find the path according to a given starting point (index of GPS data set) and distance
    

    """
    #@parameter {list} gpsData: GPS data list
    #@parameter {int} startIdx: the starting index for searching the gpsData list
    #@parameter {float} distance: in kilometer
    #@return (index, time)
    pathDist = 0
    preGPS = gpsData[startIdx]
    print preGPS
    index = startIdx
    for gps in gpsData[startIdx+1:]:
        tempDist = Haversine(preGPS[1][0], preGPS[1][1], gps[1][0], gps[1][1])
        pathDist += tempDist
        preGPS = gps
        index += 1
        if pathDist >= distance:
            break
    print "Dist: " + str(pathDist)
    return index, gpsData[index][0]