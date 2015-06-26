import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from parameter import GRID_DISTANCE
from Map.haversine import haversine
from shapely.geometry import LineString
#import numpy as np


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
          (GPSPoint linked list) region:
              the GPS data of the region
        """
        self.region = region
        self.regionList = region.toList()
        self.CloseRegionList = region.toList()
        self.CloseRegionList.append((region.lat, region.lng))

        ### find the borders ###
        pointer = self.region
        self.top    = self.region.lat
        self.bottom = self.region.lat
        self.right  = self.region.lng
        self.left   = self.region.lng
        while(pointer != None):
            if pointer.lat > self.top:
                self.top = pointer.lat
            if pointer.lat < self.bottom:
                self.bottom = pointer.lat
            if pointer.lng > self.right:
                self.right = pointer.lng
            if pointer.lng < self.left:
                self.left = pointer.lng
            pointer = pointer.next


    def findInnerGrid(self, gridSize=GRID_DISTANCE):
        """
        Find the inner grid within a region

        Args:
          (GPSPoint linked list) region: GPS data of a region 
          (float) gridSize: the length (in km) of the sides of all grids           
        Return:
          (list) gridPoint: a list of GPSPoints that are within the region
        """ 
        ### find the for corner in the rectangle that contains the region ###
        TopRight = GPSPoint(top, right)
        TopLeft  = GPSPoint(top, left)
        BotRight = GPSPoint(bottom, right)
        BotLeft  = GPSPoint(bottom, left)
   

        ### calculate the number of grid for width and height ###
        #find the distance (km) of two sides
        width = haversine(TopRight.lat, TopRight.lng,
                          TopLeft.lat, TopLeft.lng)
        height = haversine(TopRight.lat, TopRight.lng,
                           BotRight.lat, BotRight.lng)
    
        #number of segmentations in width and height
        numWidth = int(width/gridSize)
        numHeight = int(height/gridSize)
        if numWidth == 0:
            numWidth = 1
        if numHeight ==0:
            numHeight = 1

        #vertical segmentation distance
        lngDiff = (TopRight.lng - TopLeft.lng)/numWidth
        #horizontal segmentation distance 
        latDiff = (TopRight.lat - BotRight.lat)/numHeight


        ### find grid point inside the region ###
        #use dynamic programming to build the grid list
        #start checking the grid points on the four sides first, 
        #then the inner grid points
        gridPoint = []
        #starting point for lng
        lng = TopLeft.lng 
        while lnb <= TopRight.lng + lngDiff*0.0001: # "+ lngDiff*0.0001" due to the inaccuracy of numerical computation
            #starting point for lat
            lat = BotRight.lat 
            while lat <= TopRight.lat+latDiff*0.0001: 
                point = GPSPoint(lat, lng)
                if self.isInnerPoint(point):
                    #if the region contains the point
                    gridPoint.append(point)
                lat += latDiff
            lng += lngDiff

        return gridPoint


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
    

