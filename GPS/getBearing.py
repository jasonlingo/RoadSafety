import math

def getBearing(start, end):
    """
    Find the compass bearing from the start to end points
   
    Args:
      (GPSPoint) start: the position of the starting point
      (GPSPoint) end: the position of the end point
    Return:
      (int) The bearing (0~360)
    """
    
    radians = math.atan2(end.lng - start.lng, end.lat - start.lat)
    bearing = radians * 180.0 / math.pi
    return bearing
