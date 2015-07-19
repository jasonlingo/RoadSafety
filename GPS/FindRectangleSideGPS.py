import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from GPS.GPSPoint import GPSPoint

def FindRectangleSideGPS(region):
    """
    Find the top, bottom, right. left of a rectangle that 
    contains the given region.

    Args:
      (GPSPoint) region: the GPS data of a region
    Return:
      (float) top, bottom, right, left: return the four 
              extreme GPS of this region.
    """

    top = region.lat
    bottom = region.lat
    right = region.lng
    left = region.lng

    while region != None:
        if region.lat > top:
            top = region.lat
        elif region.lat < bottom:
            bottom = region.lat
        
        if region.lng > right:
            right = region.lng
        elif region.lng < left:
            left = region.lng
        region = region.next

    return (top, bottom, right, left)