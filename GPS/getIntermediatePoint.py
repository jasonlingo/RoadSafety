import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint

def getIntermediatePoint(start, end, cutNum):
    """
    Get a list of intermediate points between the start and end points.
    Cut the path into cutNum lines

    Args:
      (GPSPoint) start: the start point
      (GPSPoint) end: the end point
      (int) cutNum: the number of cuts
    Return:
      (list) GPS points
    """
    # Calculate the amount of difference of each segmentation
    latDif = (end.lat - start.lat) / cutNum
    lngDif = (end.lng - start.lng) / cutNum

    gpsList = []
    for i in xrange(cutNum): 
        # Create the start and end points of each segmentation
        startPt = GPSPoint(start.lat + latDif * i, start.lng + lngDif * i)
        endPt = GPSPoint(start.lat + latDif * (i + 1), start.lng + lngDif * (i + 1))
        gpsList.append((startPt, endPt))
        
    return gpsList    