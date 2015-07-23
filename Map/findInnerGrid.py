import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import GRID_DISTANCE
from GPS.GPSPoint import GPSPoint 
from GPS.Haversine import Haversine
from GPS.FindRectangleSideGPS import FindRectangleSideGPS
from shapely.geometry import LineString


def findInnerGrid(region, recTopRight=None, recTopLeft=None, recBotRight=None, recBotLeft=None):
    """
    Find the inner grid within a region.

    Args:
      (GPSPoint) region: a list of GPS data of a region.
      (GPSPoint) recTopRight, recTopLeft, recBotRight, recBotLeft: 
                 the GPS points of the four corners of the smallest 
                 rectangle containing the region.
    Return:
      (list) gridPoint: a list of GPSPoints that are within the region.
    """ 

    if recTopRight == None or recTopLeft == None or \
       recBotRight == None or recBotLeft == None:
        # Find the top, bottom, right, left points of the smallest 
        # rectangle containing thie region.
        (top, bottom, right, left) = FindRectangleSideGPS(region)   

        # Create the four corners' GPSPoint.
        recTopRight = GPSPoint(top, right)
        recTopLeft  = GPSPoint(top, left)
        recBotRight = GPSPoint(bottom, right)
        recBotLeft  = GPSPoint(bottom, left)

    # Calculate the length (km) of two sides of the given rectangle.
    width = Haversine(recTopRight.lat, recTopRight.lng,
                      recTopLeft.lat, recTopLeft.lng)
    height = Haversine(recTopRight.lat, recTopRight.lng,
                       recBotRight.lat, recBotRight.lng)
    
    # Number of segmentations. Each segmentation has length of GRID_DISTANCE, 
    # and the last grid will use the residual length.
    numWidth = max(1, int(width) / GRID_DISTANCE)
    numHeight = max(1, int(height) / GRID_DISTANCE)

    # Vertical segmentation distance.
    lngDiff = (recTopRight.lng - recTopLeft.lng) / numWidth

    # Horizontal segmentation distance.
    latDiff = (recTopRight.lat - recBotRight.lat) / numHeight

    # Start to find grid points in the region.
    gridPoint = []
    lng = recTopLeft.lng
    regionList = region.toList()
    while(lng <= recTopRight.lng):
        lat = recBotRight.lat
        while(lat <= recTopRight.lat):
            point = GPSPoint(lat, lng)
            if containPoint(regionList, point):
                # The region contains this point, append it 
                # to the gridPoint list.
                gridPoint.append(point)
            lat += latDiff
        lng += lngDiff

    return gridPoint



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


   