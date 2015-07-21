import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Util.kml import KmzParser
from Map.findInnerGrid import findInnerGrid
from GPS.GPSPoint import GPSPoint
from Map.GridMap import GridMap

class GetRegionStreetView:
    """
    Get street view images of major roads in a region/city.
    1. Create a grid map for this region.
    2. Get directions from Google Direction API
    """

    def __init__(self, region):
        """
        Constructor

        Args:
          (GPSPoint) region: the linked list of the GPS data of this 
                             region.
        """
        self.region = region
        
        # Create a RegionMap
        self.Map = GridMap(self.region)

        # Find the inner grid in this grid map
        self.gridPoint = findInnerGrid(self.region)

        

    def getStreetView(self):
        pass









        