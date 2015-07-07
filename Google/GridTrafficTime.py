import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from Map.findInnerGrid import findInnerGrid
from Google.Direction import getDirection
from Google.sumDirectionTime import sumDirectionTime
from time import sleep
from Google.showGridMap import showGridMap



def GridTrafficTime(region):
    """
    Calculate the traffic time of grid point in a given region

    Args:
      (Linked list) region: a linked list of GPS node of a region
    """
    #build a rectangle by find the most top, right, left, and bottom of the GPS nodes.
    pointer = region
    top = region
    bottom = region
    left = region
    right = region
    while (pointer != None):
        if pointer.lat > top.lat:
            top = pointer
        if pointer.lat < bottom.lat:
            bottom = pointer
        if pointer.lng > right.lng:
            right = pointer
        if pointer.lng < left.lng:
            left = pointer
        pointer = pointer.next

    #
    recTopRight = GPSPoint(top.lat, right.lng)
    recTopLeft  = GPSPoint(top.lat, left.lng)
    recBotRight = GPSPoint(bottom.lat, right.lng)
    recBotLeft  = GPSPoint(bottom.lat, left.lng)

    regionList = []
    while(region != None):
        regionList.append((region.lat, region.lng))
        region = region.next

    #find the inner point in the region
    gridPoint = findInnerGrid(regionList, recTopRight, recTopLeft, recBotRight, recBotLeft) 

    #get directions for every two nodes in gridPoint
    #ask before perform getting directions since the total 
    #number of direction might be very large    
    print "Total number of directions: " + str(len(gridPoint)*(len(gridPoint)-1)/2)
    continue_flag = raw_input("Continue? (Y/N):")
    if continue_flag == "n" or continue_flag == "N":
        return;

    directions= []
    for i, source in enumerate(gridPoint):
        sys.stderr.write(".")
        sourceStr = str(source.lat) + "," + str(source.lng)
        for destination in gridPoint[i+1:]:
            destStr = str(destination.lat) + "," + str(destination.lng)
            directions.append(getDirection(sourceStr,destStr))
            sleep(0.6) #2 requests per second for free account

    longestTimeDirection = sumDirectionTime(directions)

    #show grid of the region and get the returned list of grid points
    showGridMap(regionList, recTopRight, recTopLeft, recBotRight, recBotLeft, gridPoint, longestTimeDirection)    


