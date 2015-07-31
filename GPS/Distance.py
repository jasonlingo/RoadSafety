import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import METER_TYPE
from math import radians, cos, sin, asin, sqrt


def Haversine(lat1, lng1, lat2, lng2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)

    Args:
      (float) lat1, lng1: the position of the first point
      (float) lat2, lng2: the position of the second point
    Return:
      (float) distance (in km) between two nodes
    """
    # Convert decimal degrees to radians 
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

    # haversine formula 
    dlng = lng2 - lng1 
    dlat = lat2 - lat1 
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    c = 2 * asin(sqrt(a)) 

    # Radius of earth in kilometers. 
    # Use 6371 for kilometers, 3956 for miles.
    if METER_TYPE == "K":
        r = 6371 
    else:
        r = 3956
    return c * r


def FindRadiusPoint(lat, lng, bearing, distance):
    
    R = 6378.1 #Radius of the Earth
    brng = 0 #Bearing is 90 degrees converted to radians.
    d = 1 #Distance in km

    #lat2  52.20444 - the lat result I'm hoping for
    #lon2  0.36056 - the long result I'm hoping for.

    lat1 = math.radians(52.20472) #Current lat point converted to radians
    lon1 = math.radians(0.14056) #Current long point converted to radians

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    print(lat2)
    print(lon2)

