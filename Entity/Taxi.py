import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPXdata import GPSPoint
from GoogleStreetView import getDirection


class Taxi(GPSPoint):
    """Taxi object"""

    def __init__(self, lat, lng, hospitals):
        """Constructor.

        Args:
          (float) lat, lng: the lat and lng of this taxi
          (GPSPoint) hospitals: a linked list of hospitals
        """
        self.lat = lat
        self.lng = lng
        self.hospitals = hospitals

        self.isEmpty = True
        self.nearestHospital = None


    def timeToLocation(self, GPS):
        """
        Calculate the time fro current location the 
        customer's location

        Args:
          (GPSPoint) GPS: the customer's lcoation
        Return:
          (int) the time (in second) to go the customer's
                location
        """
        pass



    def toNearestHospital(self):
        """
        Find the distance between current location and 
        the nearest hospital

        Return:
          (GPSPoint) return the direction from current location 
                     to the nearest hospital
        """
        #the time to hospital
        Hduration = float("inf")
        self.nearestHospital = None

        pointer = self.hospitals
        curLoc = str(self.lat) + "," + str(self.lng)
        while pointer != None:
            hosLoc = str(pointer.lat) + "," + str(pointer.lng)
            direction = getDirection(curLoc, hosLoc)
            duration = direction.getTotalDuration()
            if duration < Hduration:
                Hdirection = direction
                Hduration = duration
                self.nearestHospital = GPSPoint(pointer.lat, pointer.lng)
            pointer = pointer.next
        return Hdirection
        #print "hos: " + str(self.nearestHospital.lat) + "," + str(self.nearestHospital.lng)



