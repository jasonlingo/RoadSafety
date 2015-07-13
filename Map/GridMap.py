import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Util.kml import kmzParser
from config import GRID_DISTANCE
from GPS.Haversine import Haversine
from Google.Direction import getDirection

class GridMap:
    """ 
    Create a grid for a given region.
    """

    def __init__(self, region):
        """
        Constructor

        Args:
          (GPSPoint) region: a linkedlist of GPSPoint of the 
                             given region.
        """
        # Parse the kmz file and get the GPSPoint linkedlist
        self.region = region
        # Find top, bottom, right, left of this rectangle
        (self.top, self.bottom, self.right, self.left) = \
                         FindRectangleSideGPS(self.region)
        # All grid points in this rectangle
        self.grids = []

        # paths of directions
        self.paths = []


    def buildGrid(self, gridSize=GRID_DISTANCE):
        """
        Generate sub-areas with each side length = areaSize in this map. There 
        might be some areas whose sides are small than areaSize.
        """
        # calculate the width and height of this MapMatrix
        width = Haversine(self.top, self.left, self.top, self.right)
        height = Haversine(self.top, self.left, self.bottom, self.left)
        
        # calculate the number of seqments of each side
        segmentW = float(width)/float(gridSize)
        segmentH = float(height)/float(gridSize)
        
        # calculate the GPS difference between each segment
        self.latDiff = (self.top - self.bottom)/segmentH
        self.lngDiff = (self.right - self.left)/segmentW

        # start generate grid points
        gridLat = self.top
        while gridLat >= self.bottom: # from top to bottom
            self.grids.append([])            
            gridLng = self.left 
            while areaLeft <= self.right: #from left to right
                self.grids[-1].append(gridPoint(gridLat, gridLng))
                gridLng += self.lngDiff
            gridLat += self.latDiff

    def getGridStreetView(self):
        """
        Get the direction from a grid point located on the side of this 
        region to the grid point on the opposite side. Also add some middle
        point in the direction in order to prevent duplications of road 
        selection.
        """
        if self.grids == []:
            return None 

        rowNum = len(self.grids)    # number of rows
        colNum = len(self.grids[0]) # number of columns

        for i in xrange(colNum):


    def showMap(self):  
        pass  



    class gridPoint:
        """
        The point of grids in this rectangle shape
        """

        def __init__(self, lat, lng):
            """Constructor"""
            # the GPS data of this grid point
            self.lat = lat
            self.lng = lng









    