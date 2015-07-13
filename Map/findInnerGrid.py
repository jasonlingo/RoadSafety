import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import GRID_DISTANCE
from Map.containPoint import containPoint
from GPS.GPSPoint import GPSPoint 
from GPS.Haversine import Haversine


def findInnerGrid(region, recTopRight=None, recTopLeft=None, recBotRight=None, recBotLeft=None):
    """
    find the inner grid within a region

    Args:
      (list) region: a list of GPS data of a region
      (GPSPoint) recTopRight, recTopLeft, recBotRight, recBotLeft:
                 the four corners of a rectangle that contains the region           
    Return:
      (list) gridPoint: a list of GPSPoints that are within the region
    """ 
   
    #add grids
    #find the distance (km) of two sides
    width = Haversine(recTopRight.lat, recTopRight.lng,
                      recTopLeft.lat, recTopLeft.lng)
    height = Haversine(recTopRight.lat, recTopRight.lng,
                       recBotRight.lat, recBotRight.lng)
    
    #number of segmentations (segmentated every 10km)
    numWidth = int(width)/GRID_DISTANCE
    numHeight = int(height)/GRID_DISTANCE

    #vertical segmentation distance
    lngDiff = (recTopRight.lng - recTopLeft.lng)/numWidth #need to deal with divide by zero

    #horizontal segmentation distance 
    latDiff = (recTopRight.lat - recBotRight.lat)/numHeight

    #find grid point
    gridPoint = []
    lng = recTopLeft.lng
    while(lng <= recTopRight.lng*1.0001):
        lat = recBotRight.lat
        while(lat <= recTopRight.lat*1.0001):
            point = GPSPoint(lat, lng)
            if containPoint(region, point):
                #if the region contains the point
                gridPoint.append(point)
            lat += latDiff
        lng += lngDiff

    return gridPoint