#to import other module from other package
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPXdata import GPSPoint
from kml import KmzParser
from Util.Map import findInnerGrid, Map



class TaxiExperiment:
    """
    When a crash happens, find the taxi that can arrive the 
    crash location with minimal time among all the taxis in 
    the region.
    """
    #(GPSPoint) the GPS data of the region
    region = None
    #(GPSPoint) the position of all taxis
    taxis = None


    def __init__(self, region_filename):
        """
        Construct the experiment

        Args:
          (String) region_filename: the location of the region 
                   file from Google MAP kmz file
        """
        self.region = KmzParser(region_filename)
        self.map = RegionMap(region)
        self.map.findInnerGrid()


    def addHospital(self, hospital_filename):
        """
        Add hospitals' locations in the region

        Args:
          (String) hospital_filename: the locations of hospitals
                   to be added into the map
        """
        pass


    def addTaxi(self, taxis_filename):
        """
        Add taxis according to the given location.
        
        Args:
          (String) taxis_filename: the location of a list of all 
                   the taxis in the region
        """
        self.taxis = KmzParser(taxis_filename)


    def addRandomTaxi(self, num):
        """
        Add num taxis at random location in the region.

        Args:
          (int) num: the number of taxis to add.
        """
        pointer = taxis.getTail()
        #pointer.next = 


    def addCrash(self, crash_filename):
        pass


    def addRandomCrash(self, num):
        pass


        



