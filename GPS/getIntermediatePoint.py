import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint

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