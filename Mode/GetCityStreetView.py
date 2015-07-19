import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Util.kml import KmzParser
from Map.findInnerGrid import findInnerGrid
from GPS.GPSPoint import GPSPoint

class GetCityStreetView:
    """
    Get street view images of major roads in a region/city.
    1. create a grid map for this region
    2. Get directions from Google direction API for grid
    """

    def __init__(self, region_filename):
        """
        Constructor

        Args:
          (String) regionFile: the filename of a region file in
                   kmz format produced by Google My Map.
        """
        # Parse the GPX data to GPSPoint linkedlist
        self.region = KmzParser(region_filename)
        # create a RegionMap
        self.Map = GridMap(self.region)
        # Find the for corners of the rectangle of this map
        self.recTopRight = GPSPoint(self.Map.top, self.Map.right)
        self.recTopLeft = GPSPoint(self.Map.top, self.Map.left)
        self.recBotRight = GPSPoint(self.Map.buttom, self.Map.right)
        self.recBotLeft = GPSPoint(self.Map.buttom, self.Map.left)

        # Find the inner grid in this grid map
        self.gridPoint = findInnerGrid(self.recTopRight, self.recTopLeft, \
                                       self.recBotRight, self.recBotLeft)

        

    def getStreetView(self):










        