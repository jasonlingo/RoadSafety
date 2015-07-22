import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
import time
from config import API_KEY
import requests, json
import time
from datetime import datetime
from pytz import timezone


def findTimeZone(gpsPoint):
    """
    Find time zone according to GPS data by using Google Time Zone API.

    Args:
      (GPSPoint) gpsPoint: the GPS of the time zone
    Return:
      time zone
    """

    # API url.
    TIMEZONE_API_URL = "https://maps.googleapis.com/maps/api/timezone/json?"
    
    #parameters for API.
    params = dict(
        location=str(gpsPoint.lat) + ',' + str(gpsPoint.lng),
        timestamp=str(time.time()),
        key=API_KEY
    )

    # Get time zone from Google time zone API.
    resp = requests.get(url=TIMEZONE_API_URL, params=params)
    
    # Transform response to json format.
    data = json.loads(resp.text)
    
    # Get time zone name from replied data.
    timezoneName = data['timeZoneId']
    
    # Set the local time zone.
    eastern = timezone('US/Eastern')
    
    # Find the current time of the location (gpsPoint).
    targetTZ = timezone(timezoneName)
    loc_dt = eastern.localize(datetime.now())
    target_dt = loc_dt.astimezone(targetTZ)
    
    # Set the time format for data to be returned.
    fmt = '%Y-%m-%d_%H-%M-%S'

    return timezoneName, target_dt.strftime(fmt)