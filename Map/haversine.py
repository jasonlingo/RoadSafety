import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lng1, lat2, lng2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)

    Args:
      (float) lat1, lng1: the GPS of the first point
      (float) lat2, lng2: the GPS of the second point
    Return:
      (int) distance (in km) between two nodes
    """
    # return {kilometer}
    # convert decimal degrees to radians 
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

    # haversine formula 
    dlng = lng2 - lng1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles, 6371 for kilometers
    return c * r