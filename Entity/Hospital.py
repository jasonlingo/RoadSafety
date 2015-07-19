import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Hospital(GPSPoint):

    def __init__(self, lat, lng, name=None, capacity=0):
        """
        Constructor

        Args:
          (float) lat, lng: the GPS location of this Hospital
          (String) name: the hospital name
          (int) capacity: the capacity (the number of patients 
                          that can be accepted) of this hospital
        """
        GPSPoint.__init__(self, lat, lng)
        self.name = name
        self.capacity = capacity
        




