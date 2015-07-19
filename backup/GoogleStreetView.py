import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from config import GPS_DISTANCE, VIDEO_FRAME_DIRECTORY, FOLDER_NAME, OUTPUT_DIRECTORY, API_KEY
from GoogleMap import showPath
from GDrive import GDriveUpload
from FileUtil import outputCSV
import urllib, urllib2
import json, requests
import webbrowser
import math
import time
import pprint
from Util.kml import KmzParser
import xml
import sys
from time import sleep





def getIntermediatePoint(start, end, cutNum):
    """
    Get a list of intermediate points between the start and end points.
    Cut the path into cutNum lines

    Args:
      start (GPSPoint): the start point
      end (GPSPoint)  : the end point
      cutNum (int)    : the number of cuts
    Return:
      a list of GPS points
    """
    latDif = (end.lat - start.lat)/cutNum
    lngDif = (end.lng - start.lng)/cutNum
    gpsList = []
    for i in xrange(cutNum): 
    	startPt = GPSPoint(start.lat+latDif*i, start.lng+lngDif*i)
    	endPt = GPSPoint(start.lat+latDif*(i+1), start.lng+lngDif*(i+1))
    	gpsList.append((startPt, endPt))
    return gpsList



def getDirection(originAdd, destAdd):
    """
    Get direction from the starting address to the destination
    
    Args:
      originAdd: the origin GPS position or address
      destAdd: the destination GPS position or address
    Return:
      a linked list of direction
    """
    #API url
    DIRECTION_API_URL = 'https://maps.googleapis.com/maps/api/directions/json?'
    #parameters for API
    params = dict(
        origin=originAdd,
        destination=destAdd,
        departure_time=str(time.strftime("%H%M%S")), #format: HHMMSS
        key=API_KEY
    )
    #get direction from Google MAP API
    resp = requests.get(url=DIRECTION_API_URL, params=params)
    #transform response to json format
    data = json.loads(resp.text)
    
    #get GPS data from json
    head = getGpsFromJson(data)
    #head.printNode()
    sleep(0.1)
    return head



