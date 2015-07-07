import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import gpxpy
import gpxpy.gpx
from TimeZoneCalibrate import TimeZoneCalibrate

def parseGPX(GPXfile):
    """
    Parse gpx file and return a list of GPS data

    Args:
      (String) GPXfile: the filename of a GPX file
    Return:
      (list) a list of GPS data
    """
    f = open(GPXfile,'r')
    gpx = gpxpy.parse(f)
    gpsData = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                gpsData.append([TimeZoneCalibrate(point.time), (point.latitude, point.longitude, point.elevation)])
                #print 'Point at ({0},{1}) -> {2}, time={3}'.format(point.latitude, point.longitude, point.elevation, point.time)
    return gpsData

