import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from config import GPS_DISTANCE, VIDEO_FRAME_DIRECTORY, FOLDER_NAME, OUTPUT_DIRECTORY, API_KEY
from Google.showPath import showPath
from Google.Drive import GDriveUpload
#import urllib, urllib2
import json, requests
#import math
import time
from Util.kml import KmzParser
import xml
from time import sleep
from Google.getGpsFromJson import getGpsFromJson


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

