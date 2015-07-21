import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import gpxpy
import gpxpy.gpx
from config import GPS_TIME_ZONE
from TimeZoneCalibrate import TimeZoneCalibrate


def parseGPX(GPXfile):
    """
    Parse gpx file and return a list of GPS data.

    Args:
      (String) GPXfile: the filename of a GPX file.
    Return:
      (list) a list of GPS data
    """
    # Open gpx file
    f = open(GPXfile,'r')
    
    # Use gpxpy function to parse the gpx data 
    gpx = gpxpy.parse(f)
    
    # Insert GPS data into a list
    gpsData = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # Append the adjusted time, latitude, longitude, 
                # and elevation of every GPS record.
                gpsData.append( [TimeZoneCalibrate(point.time, GPS_TIME_ZONE),
                                (point.latitude, point.longitude, point.elevation)])
    
    return gpsData

