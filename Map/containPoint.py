import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

#import pygmaps 
#import webbrowser
#import googlemaps
#from config import OUTPUT_DIRECTORY, GRID_DISTANCE
#from datetime import datetime, date, time
#from GPS.GPSPoint import GPSPoint 
from shapely.geometry import LineString


def containPoint(region, checkPoint):
    """ 
    Check whether the region contains the point

    Args:
      (list) region: a list of GPS points of a region
      (GPSPoint) checkPoint: a point to be checked
    Return:
      (boolean) True if the region contains the point; False otherwise
    """
    #1. Find the highest point on the region line and add 0.001 to its latitude,
    #   then the new point must be a point outside the region.
    #2. Connect the new point with the checkPoint,
    #   check whether the line across the region line segmentation,
    #3. If the line across the region line for odd times, then the point is in the region

    #find the highest poin
    highest = region[0]
    for point in region:
        if point[0] > highest[0]:
            highest = point
    highest = (highest[0]+0.001, highest[1])
    intersectNum = 0
    pre = region[0]
    for point in region[1:]:
        line1 = LineString([(pre[0], pre[1]), (point[0], point[1])])
        line2 = LineString([(highest[0], highest[1]), (checkPoint.lat, checkPoint.lng)])
        if str(line1.intersection(line2)) != "GEOMETRYCOLLECTION EMPTY":
            intersectNum += 1
        pre = point

    return intersectNum%2 == 1