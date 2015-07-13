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
      a linked list of direction
    """
    #API url
    DIRECTION_API_URL = 'https://maps.googleapis.com/maps/api/directions/json?'
    #parameters for API
    print "get direction..."
    params = dict(
        origin=originAdd,
        destination=destAdd,
        waypoints=waypointsConvert(waypoints), # convert waypoints
        unit='metric', # return distance in meter
        departure_time=str(time.strftime("%H%M%S")), #format: HHMMSS
        key=API_KEY
    )
    print params
    #get direction from Google MAP API
    resp = requests.get(url=DIRECTION_API_URL, params=params)
    #transform response to json format
    data = json.loads(resp.text)
    
    #get GPS data from json
    head = getGpsFromJson(data)
    #head.printNode()
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
    waypoints = ""
    first = True
    while ways != None:
        if not first:
            waypoints ++ "|"
            first = False
        waypoints += str(ways.lat) + "," + str(ways.lng)
    return waypoints



