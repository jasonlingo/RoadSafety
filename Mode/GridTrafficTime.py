import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from GPS.FindRectangleSideGPS import FindRectangleSideGPS
from Google.sumDirectionTime import sumDirectionTime
from Google.showGridMap import showGridMap
from Google.Direction import getDirection
from Map.findInnerGrid import findInnerGrid
from time import sleep


def GridTrafficTime(region):
    """
    Divide the region into grids and get the point-to-point traffic 
    time using Google Direction API.

    Args:
      (GPSPoint) region: a linked list of GPS node of a region
    """
    # Build a rectangle by finding the most top, right, left, and 
    # bottom of the GPS nodes that contain the given region.
    (top, bottom, right, left) = FindRectangleSideGPS(region)

    # Create the four corners' GPSPoint
    recTopRight = GPSPoint(top, right)
    recTopLeft  = GPSPoint(top, left)
    recBotRight = GPSPoint(bottom, right)
    recBotLeft  = GPSPoint(bottom, left)

    # Find the inner point in the region
    gridPoint = findInnerGrid(region,   
                              recTopRight, 
                              recTopLeft, 
                              recBotRight,
                              recBotLeft) 

    # Get directions for every two nodes in gridPoint.
    # Ask before start getting directions since the total 
    # number of direction might be very large.    
    print "Total number of directions: " + str(len(gridPoint) * (len(gridPoint) - 1) / 2)
    continue_flag = raw_input("Continue? (Y/N):")
    if continue_flag == "n" or continue_flag == "N":
        return;

    directions= []
    for i, source in enumerate(gridPoint):
        # Show the progress on screen.
        sys.stderr.write(".")

        sourceStr = str(source.lat) + "," + str(source.lng)
        for destination in gridPoint[i + 1:]:
            # We will query the directions for the combination of every two 
            # grid points. For (A, B) and (B, A), we only query one of them 
            # in order to keep the total number of query smaller.
            # A and B is the grid points.
            destStr = str(destination.lat) + "," + str(destination.lng)
            directions.append(getDirection(sourceStr, destStr))
            
            # To avoid exceed the limit on the requests per second.
            # for free Google API account.
            sleep(0.6) 

    # Find the route with the longest traffic time.
    longestTimeDirection = sumDirectionTime(directions)

    # Show grid of the region and get the returned list of grid points.
    showGridMap(region.toList(), recTopRight, recTopLeft, recBotRight, recBotLeft, gridPoint, longestTimeDirection)    


