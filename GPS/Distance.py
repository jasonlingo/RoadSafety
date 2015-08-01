import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import METER_TYPE, EARTH_RADIUS_MILE, EARTH_RADIUS_KM
from math import radians, cos, sin, asin, sqrt, degrees, atan2


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

    # The radius of earth in kilometers. 
    if METER_TYPE == "K":
        r = EARTH_RADIUS_KM # The radius of earth in kilometers.
    else:
        r = EARTH_RADIUS_MILE # The radius of earth in miles.
    return c * r


def FindRadiusPoint(lat, lng, bearing, distance):
    """
    Given a point (with its latitude and longitude), find another point 
    that has a distance equals to the given "distance" parameter 
    between them and has the bearing equals to the given "bearing" parameter.

    Args:
      (float) lat, lng: the latitude and longitude of the given point.
      (float) bearing: the bearing between the given point and the point 
              this function is going to find.
              north=90; east=90; west=-90; south=180
      (float) distance: the distance between two points.
    Return:
      (float) lat2, lng2: the found point's latitude and longitude.
    """
    # The radius of earth in kilometers. 
    if METER_TYPE == "K":
        r = EARTH_RADIUS_KM # The radius of the Earth in kilometers.
    else:
        r = EARTH_RADIUS_MILE # The radius of the Earth in miles.


    lat1 = radians(lat) # Current latitude point converted to radians
    lng1 = radians(lng) # Current longitude point converted to radians
    bearing = radians(bearing) # Current bearing converted to radians

    lat2 = asin( sin(lat1) * cos(distance / r) +
           cos(lat1) * sin(distance / r) * cos(bearing))

    lng2 = lng1 + atan2(sin(bearing) * sin(distance / r) * cos(lat1),
                  cos(distance / r) - sin(lat1) * sin(lat2))

    lat2 = degrees(lat2)
    lng2 = degrees(lng2)

    return lat2, lng2

