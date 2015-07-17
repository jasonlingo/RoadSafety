import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import GRID_DISTANCE
from Map.containPoint import containPoint
from GPS.GPSPoint import GPSPoint 
from GPS.Haversine import Haversine


def findInnerGrid(region, recTopRight=None, recTopLeft=None, recBotRight=None, recBotLeft=None):
    """
    Find the inner grid within a region

    Args:
      (list) region: a list of GPS data of a region
      (GPSPoint) recTopRight, recTopLeft, recBotRight, recBotLeft:
                 the four corners of a rectangle that contains the region           
    Return:
      (list) gridPoint: a list of GPSPoints that are within the region
    """ 
    # Find the length (km) of two sides of the given rectangle
    width = Haversine(recTopRight.lat, recTopRight.lng,
                      recTopLeft.lat, recTopLeft.lng)
    height = Haversine(recTopRight.lat, recTopRight.lng,
                       recBotRight.lat, recBotRight.lng)
    
    # Number of segmentations. Each segmentation has length of GRID_DISTANCE, 
    # and the last grid will use the remainder length.
    numWidth = max(1, int(width)/GRID_DISTANCE)
    numHeight = max(1, int(height)/GRID_DISTANCE)

    # Vertical segmentation distance
    lngDiff = (recTopRight.lng - recTopLeft.lng)/numWidth

    # Horizontal segmentation distance 
    latDiff = (recTopRight.lat - recBotRight.lat)/numHeight

    # Find grid point
    gridPoint = []
    lng = recTopLeft.lng
    while(lng <= recTopRight.lng * 1.0001):
        lat = recBotRight.lat
        while(lat <= recTopRight.lat * 1.0001):
            point = GPSPoint(lat, lng)
            if containPoint(region, point):
                # If the region contains the point
                gridPoint.append(point)
            lat += latDiff
        lng += lngDiff

    return gridPoint