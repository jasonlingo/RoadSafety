import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from Google.Direction import getDirection
from Entity.Taxi import Taxi

class Crash(GPSPoint):
    """Crash object"""

    def __init__(self, lat, lng, hospitals, next=None):
        """Constructor.
        
        Args:
          (float) lat, lng: the lat and lng of this crash
          (GPSPoint) hospitals: a linked list of hospitals
        """
        GPSPoint.__init__(self, lat, lng)
        #self.lat = lat
        #self.lng = lng
        self.isSaved = False
        self.hospitals = hospitals
        self.nearestHospital = None
        self.next = next
        #find the nearest hospital
        #print "cur: " + str(self.lat) +","+ str(self.lng)
        #self.getNearestHospital()


    def getNearestHospital(self):
        """
        Find the distance between current location and 
        the nearest hospital
        """
        self.Hdistance = float("inf")
        self.nearestHospital = None
        pointer = self.hospitals
        curLoc = str(self.lat) + "," + str(self.lng)
        while pointer != None:
            hosLoc = str(pointer.lat) + "," + str(pointer.lng)
            direction = getDirection(curLoc, hosLoc)
            dist = 0
            while direction != None:
                dist += direction.distance
                direction = direction.next
            if dist < self.Hdistance:
                self.Hdistance = dist
                self.nearestHospital = GPSPoint(pointer.lat, pointer.lng)
            pointer = pointer.next
        #print "hos: " + str(self.nearestHospital.lat) + "," + str(self.nearestHospital.lng)




