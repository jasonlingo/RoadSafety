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
    Check whether the region contains the point.
    1. Find the highest point on the region line and add 0.001 to its latitude,
       then the new point must be a point outside the region.
    2. Connect the new point with the checkPoint, then check whether 
       the line across the region lines.
    3. If the total number of that the line across the region lines 
       is a odd number, then the checkPoint is inside the region.
    
    Args:
      (list) region: a list of GPS points of a region
      (GPSPoint) checkPoint: a point to be checked
    Return:
      (boolean) True if the region contains the point; False otherwise
    """

    # Find the highest point.
    highest = region[0]
    for point in region[1:]:
        if point[0] > highest[0]:
            highest = point
    highest = (highest[0] * 1.0001, highest[1])

    # The line connects the ckeckPoint and outside point
    line1 = LineString([(highest[0], highest[1]), (checkPoint.lat, checkPoint.lng)])
    
    # Initialize the number of intersection of the region line and 
    # the line that connects the outside point and the checkPoint.
    intersectNum = 0

    # Start counting the times of the line intersects the region lines.
    # Initialize previous point (pre) to the last point in the region list 
    # in order to connect the last and first point in the list.
    pre = region[-1]
    for point in region:
        line2 = LineString([(pre[0], pre[1]), (point[0], point[1])])
        if str(line1.intersection(line2)) != "GEOMETRYCOLLECTION EMPTY":
            # Has at least one intersection.
            intersectNum += 1
        pre = point

    return intersectNum % 2 == 1