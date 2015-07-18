import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import GRID_DISTANCE
from GPS.Haversine import Haversine
from shapely.geometry import LineString
from GPS.FindRectangleSideGPS import FindRectangleSideGPS

class RegionMap():
    """The map of a region"""
    #the GPS data of the region in this map
    region = None
    #the list of all the GPS points in region linked list
    regionList = None
    #have the additional line connects the last point with the first point
    CloseRegionList = None 
    #the 
    top    = None
    bottom = None
    right  = None
    left   = None
    
    matrix = None

    def __init__(self, region):
        """
        Construct the map by the region
        
        Args: 
          (GPSPoint linkedlist) region:
              the GPS data of the region
        """
        self.region = region
        self.regionList = region.toList()
        self.CloseRegionList = region.toList()
        self.CloseRegionList.append((region.lat, region.lng))

        ### find the borders ###

        (self.top, self.bottom, self.right, self.left) = \
                          FindRectangleSideGPS(self.region)


    def isInnerPoint(self, checkPoint):
        """ 
        Check whether the region contains the checkPoint

        Args:
          (GPSPoint) checkPoint: a point to be checked
        Return:
          (boolean) True if the region contains the point; False otherwise
        """
        #1. Find a point outside the region
        #2. Connect the new point with the checkPoint,
        #   check whether the line across the region line segmentation,
        #3. If the line across the region line for odd times, then the point is in the region

        ### find a point outside the region ###
        highest = (self.top*1.0001, self.right*1.0001)
        #the number of intersection of the region line and 
        #the line connects the outside point and the checkPoint
        intersectNum = 0
        #initialize

        pre = self.CloseRegionList[0]
        #the line connects the ckeckPoint and outside point
        line1 = LineString([(highest[0], highest[1]), (checkPoint.lat, checkPoint.lng)])         
        for point in self.CloseRegionList[1:]:
            #region line
            line2 = LineString([(pre[0], pre[1]), (point[0], point[1])]) 
            if str(line1.intersection(line2)) != "GEOMETRYCOLLECTION EMPTY":
                intersectNum += 1
            pre = point

        return intersectNum%2 == 1


    class gridNode:
        """The data structure that stores the grid node infor"""
        #GPS data
        lat = None
        lng = None
        #whether the node is inside the region
        isInnerNode = None

        def __init__(self, lat, lng):
            """Construct the node"""
            self.lat = lat
            self.lng = lng
    

