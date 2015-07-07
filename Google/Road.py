#Google MAP Road API
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS import GPSPoint
from config import API_KEY
import json, requests
from pprint import pprint
from GoogleStreetView import getDirection
from Map.haversine import haversine

def getRoadGPS(GPS):
    """
    Use Google MAP Road API to get the nearest road GPS 
    for the given GPS location

    Args:
      (GPSPoint) GPS: the given location for that we want 
                 to find the nearest road's GPS data 
    Return:
      (GPSPoint) return the nearest road's GPS 
    """
    ROAD_API_URL = "https://roads.googleapis.com/v1/snapToRoads?"
    #generate path parameter
    pathStr = ""
    pointer = GPS
    while pointer != None:
        pathStr += str(pointer.lat)+","+str(pointer.lng)
        if pointer.next != None:
            pathStr += "|"
        pointer = pointer.next

    params = dict(
        path=pathStr,
        interpolate="true",
        key=API_KEY
    )
    #get road GPS 
    resp = requests.get(url=ROAD_API_URL, params=params)
    data = json.loads(resp.text)
    if data != {}:
        road = data['snappedPoints']
        roadGPS = GPSPoint(road[0]['location']['latitude'], road[0]['location']['longitude'])
        pointer = roadGPS
        for gps in road[1:]:
            lat = gps['location']['latitude']
            lng = gps['location']['longitude']
            pointer.next = GPSPoint(lat, lng)
            pointer.distance = haversine(roadGPS.lat, roadGPS.lng, lat, lng)*1000
            pointer = pointer.next
        return roadGPS 

    return GPS


