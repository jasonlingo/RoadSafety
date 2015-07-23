#Google MAP Road API
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from GPS.Haversine import Haversine
from config import API_KEY
from pprint import pprint
import json, requests
from time import sleep

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
    # The url for Google Road API.
    ROAD_API_URL = "https://roads.googleapis.com/v1/snapToRoads?"
   

    # Initialize path parameter list.
    pathStrs = []

    # Generate path parameters.
    pathStr = ""
    pointer = GPS

    # The points allowed in Google Road API is 100.
    # Count the number of points. If it is larger than 100, divide the 
    # points into different queries and concatenate them later.
    numOfpoint = 0

    # Start concatenating GPS points into a string.
    tempList = []
    while pointer != None:
        numOfpoint += 1
        pathStr = str(pointer.lat) + "," + str(pointer.lng)
        tempList.append(pathStr)
        pointer = pointer.next
        if numOfpoint == 100:
            pathStr = "|".join(tempList)
            pathStrs.append(pathStr)

            # Reset data
            i = 0;
            tempList = []

    if len(tempList) > 0:
        pathStr = "|".join(tempList)
        pathStrs.append(pathStr)

    # For every path data in pathStrs, create its parameters for 
    # Google Road API.
    paramList = []
    for pathStr in pathStrs:
        params = dict(
            path=pathStr,
            interpolate="true",
            key=API_KEY
        )
        paramList.append(params)


    # For every parameters in paramList, get its road GPS.
    headFlag = False
    startIdx = 0
    for params in paramList:
        resp = requests.get(url=ROAD_API_URL, params=params)
        data = json.loads(resp.text)
    
        if data != {}:
            try:
                road = data['snappedPoints']
                if not headFlag:
                    roadGPS = GPSPoint(road[0]['location']['latitude'], road[0]['location']['longitude'])
                    pointer = roadGPS
                    headFlag = True
                    startIdx = 1
                else:
                    startIdx = 0

                for gps in road[startIdx:]:
                    lat = gps['location']['latitude']
                    lng = gps['location']['longitude']
                    pointer.next = GPSPoint(lat, lng)
                    pointer.distance = Haversine(pointer.lat, pointer.lng, lat, lng) * 1000 # Convert to meter.
                    pointer = pointer.next
            except:
                
                print "An error happened while parsing the replied data from Google Road API!!"
                print data
                return GPS

    return roadGPS


