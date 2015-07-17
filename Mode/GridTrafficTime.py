import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from Map.findInnerGrid import findInnerGrid
from Google.Direction import getDirection
from Google.sumDirectionTime import sumDirectionTime
from Google.showGridMap import showGridMap
from time import sleep



def GridTrafficTime(region):
    """
    Calculate the traffic time of grid point in a given region

    Args:
      (Linked list) region: a linked list of GPS node of a region
    """
    # Build a rectangle by finding the most top, right, left, and 
    # bottom of the GPS nodes that contain the given region
    pointer = region
    top    = GPSPoint(region.lat, region.lng)
    bottom = GPSPoint(region.lat, region.lng)
    left   = GPSPoint(region.lat, region.lng)
    right  = GPSPoint(region.lat, region.lng)
    while (pointer != None):
        if pointer.lat > top.lat:
            top.lat = pointer.lat
            top.lng = pointer.lng
        elif pointer.lat < bottom.lat:
            bottom.lat = pointer.lat
            bottom.lng = pointer.lng
        
        if pointer.lng > right.lng:
            right.lat = pointer.lat
            right.lng = pointer.lng
        elif pointer.lng < left.lng:
            left.lat = pointer.lat
            left.lng = pointer.lng
        pointer = pointer.next

    # Create the four corners' points
    recTopRight = GPSPoint(top.lat, right.lng)
    recTopLeft  = GPSPoint(top.lat, left.lng)
    recBotRight = GPSPoint(bottom.lat, right.lng)
    recBotLeft  = GPSPoint(bottom.lat, left.lng)

    regionList = []
    while(region != None):
        regionList.append((region.lat, region.lng))
        region = region.next

    # Find the inner point in the region
    gridPoint = findInnerGrid(regionList, recTopRight, recTopLeft, recBotRight, recBotLeft) 

    # Get directions for every two nodes in gridPoint
    # Ask before start getting directions since the total 
    # number of direction might be very large    
    print "Total number of directions: " + str(len(gridPoint) * (len(gridPoint) - 1) / 2)
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
            # To avoid exceed the limit on the requests per second 
            # for free Google API account
            sleep(0.6) 

    # Find the route with the longest traffic time
    longestTimeDirection = sumDirectionTime(directions)

    # Show grid of the region and get the returned list of grid points
    showGridMap(regionList, recTopRight, recTopLeft, recBotRight, recBotLeft, gridPoint, longestTimeDirection)    


