import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import API_KEY
from Google.getGpsFromJson import getGpsFromJson
from GPS.GPSPoint import GPSPoint
from time import sleep
import json, requests
import time


def getDirection(originAdd, destAdd, waypoints=None):
    """
    Get direction from the starting address to the destination
    
    Args:
      (String) originAdd: the origin GPS position or address
      (String) destAdd: the destination GPS position or address
      (GPSPoint) waypoints: the middle points between source and
                            destination points.
    Return:
      (GPSPoint) a linked list of direction
    """
    # API url
    DIRECTION_API_URL = 'https://maps.googleapis.com/maps/api/directions/json?'
    # Parameters for API
    params = dict(
        origin=originAdd,
        destination=destAdd,
        waypoints=waypointsConvert(waypoints), # convert waypoints
        unit='metric', # return distance in meter
        departure_time=str(time.strftime("%H%M%S")), #format: HHMMSS
        key=API_KEY
    )

    # Get direction from Google MAP API
    resp = requests.get(url=DIRECTION_API_URL, params=params)
    # Transform response to json format
    data = json.loads(resp.text)
    # Get GPS data from json
    head = getGpsFromJson(data)
    # For the request limit by Google Direction API
    sleep(0.1)

    return head


def waypointsConvert(ways):
    """
    Convert waypoints from GPSPoint linkedlist to a string by 
    concatenating every consecutive points with a '|' word 
    between them.

    Args:
      (GPSPoint) ways: the points of intermediate points between 
                       source and destination points.
    Return:
      (String) the concatenated waypoints string.
    """
    # Initialize waypoints string
    waypoints = ""
    # First point doesn't have to add "|" before it
    first = True
    while ways != None:
        if first:
            first = False
        else:
            # Add "|" between every two waypoints
            waypoints += "|"
        waypoints += str(ways.lat) + "," + str(ways.lng)
        ways = ways.next
    return waypoints



