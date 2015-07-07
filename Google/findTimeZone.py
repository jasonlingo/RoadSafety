import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import gpsPoint


def findTimeZone(gpsPoint):
    """
    Find time zone according to GPS data by using Google Time Zone API

    Args:
      (GPSPoint) gpsPoint: the GPS of the time zone
    Return:
      time zone
    """

    TIMEZONE_API_URL = "https://maps.googleapis.com/maps/api/timezone/json?"
    #parameters for API
    params = dict(
        location=str(gpsPoint.lat) + ',' + str(gpsPoint.lng),
        timestamp=str(time.time()),
        key=API_KEY
    )
    #get time zone from Google time zone API
    resp = requests.get(url=TIMEZONE_API_URL, params=params)
    #transform response to json format
    data = json.loads(resp.text)
    #get time zone from dict data
    timezoneName = data['timeZoneId']
    #set the time format
    fmt = '%Y-%m-%d_%H-%M-%S'
    #set the local time zone
    eastern = timezone('US/Eastern')
    #find the current time of the target time zone
    targetTZ = timezone(timezoneName)
    loc_dt = eastern.localize(datetime.now())
    target_dt = loc_dt.astimezone(targetTZ)
    
    return timezoneName, target_dt.strftime(fmt)