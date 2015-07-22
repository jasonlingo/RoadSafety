import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint

class Car(GPSPoint):
    """
    A class of car object
    """

    def __init__(self, lat, lng, next=None, speed=1.0, size=1.0, available=True):
        """
        Constructor
        """
        GPSPoint.__init__(self, lat, lng)

        # The multiplier of the speed. Different types of cars
        # will have different priority on the road. Ex: an ambulance
        # will generally have higher priority than a taxi, leading to 
        # shorter traffic time.
        self.speed = speed

        # Different types of car will have different sizes, thus will
        # have different capacities.
        self.size = size

        # Whether this car is able to take customers.
        self.available = available

    


