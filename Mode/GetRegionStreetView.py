import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Map.findInnerGrid import findInnerGrid
from GPS.GPSPoint import GPSPoint
from Map.GridMap import GridMap
from config import GRID_DISTANCE, OUTPUT_DIRECTORY

class GetRegionStreetView:
    """
    Get street view images of major roads in a region/city.
    1. Create a grid map for this region.
    2. Get directions from Google Direction API.
    """

    def __init__(self, region):
        """
        Constructor.

        Args:
          (GPSPoint) region: the linked list of the GPS data of this 
                             region.
        """
        # Keep the region linked list.
        self.region = region
        
        # Create a grid map that can store a 
        self.Map = GridMap(self.region, GRID_DISTANCE)

        # Find the inner grid in this grid map
        #self.gridPoint = findInnerGrid(self.region)

        # Start getting street view images of this region.
        self.Map.getGridStreetView(OUTPUT_DIRECTORY + "region_street_image/")


        

    def getStreetView(self):
        pass









        