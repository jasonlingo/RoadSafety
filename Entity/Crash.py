import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint


class Crash(GPSPoint):
    """
    A class of crash object.
    """

    def __init__(self, lat, lng, next=None, crashDate=None, crashTime=None):
        """Constructor.
        
        Args:
          (float) lat, lng: the lat and lng of this crash
          (GPSPoint) hospitals: a linked list of hospitals
        """
        GPSPoint.__init__(self, lat, lng, 0, 0, next)

        # To make whether the patient of this crash is saved.
        self.isSaved = False

        # The date and time of this crash.
        self.crashDate = crashDate
        self.crashTime = crashTime
 