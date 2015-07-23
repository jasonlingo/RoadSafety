import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Entity.Car import Car
from Google.Direction import getDirection
from GPS.GPSPoint import GPSPoint


class Taxi(Car):
    """Taxi class"""

    def __init__(self, lat, lng, hospitals):
        """
        Construct a Taxi object.

        Args:
          (float) lat, lng: the latitude and longitude of this taxi.
          (GPSPoint) hospitals: a linked list of hospitals.
        """
        Car.__init__(self, lat, lng)

        # Keep the hospital list
        self.hospitals = hospitals

        # The nearest hospital to this taxi.
        # self.nearestHospital = None


    def toNearestHospital(self):
        """
        Find the distance between current location and the nearest hospital.

        Return:
          (GPSPoint) return the direction from current location to the 
                     nearest hospital.
        """
        # Initialize the time to the neareset hospital.
        Hduration = float("inf")

        # Initialize nearestHospital
        self.nearestHospital = None

        # The string of the GPS data of the current location.
        curLoc = str(self.lat) + "," + str(self.lng)
        
        # For every hospital in the list, check the traffic time from the 
        # current location to it, and find the one with the shortest traffic 
        # time.
        pointer = self.hospitals
        while pointer != None:
            # The string of the GPS data of this hospital.
            hosLoc = str(pointer.lat) + "," + str(pointer.lng)

            # Get a direction from the current location to this hospital using 
            # Google Direction API.
            direction = getDirection(curLoc, hosLoc)

            # Initialize the duration to be float("inf")
            # in order to prevent this direction from being recorded
            # as the shortest direction if the direction is None
            # replied from getDirection().
            duration = float("inf")
            if direction != None:
                # Get the traffic time of this direction.
                duration = direction.getTotalDuration()
            
            if duration < Hduration:
                # The traffic time is less than shortest traffic time so far, 
                # so update the shortest traffic time data.
                Hdirection = direction
                Hduration = duration
                self.nearestHospital = GPSPoint(pointer.lat, pointer.lng)
            pointer = pointer.next
    
        return Hdirection
    



