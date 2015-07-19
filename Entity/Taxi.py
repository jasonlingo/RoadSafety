import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Entity.Car import Car
from Google.Direction import getDirection
from GPS.GPSPoint import GPSPoint


class Taxi(Car):
    """Taxi class"""

    def __init__(self, lat, lng, hospitals):
        """Constructor.

        Args:
          (float) lat, lng: the lat and lng of this taxi
          (GPSPoint) hospitals: a linked list of hospitals
        """
        Car.__init__(self, lat, lng)
        #self.lat = lat
        #self.lng = lng
        self.hospitals = hospitals

        self.isEmpty = True
        self.nearestHospital = None


    def TimeToCustomer(self, customerGPS):
        """
        The time for this taxi to go from current location the 
        customer's location.

        Args:
          (GPSPoint) customerGPS: the customer's location
        Return:
          (int) time (in second) to the customer
        """
        # Using Google direction API to get the traffic time.



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



