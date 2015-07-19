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