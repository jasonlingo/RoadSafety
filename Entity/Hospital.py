import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from datetime import time
import datetime

class Hospital(GPSPoint):

    def __init__(self, lat, lng, name=None, capacity=10, OpenTime=time(0, 0, 0, 0), CloseTime=time(0, 0, 0, 0)):
        """
        Construct a hospital

        Args:
          (float) lat, lng: the GPS location of this Hospital
          (String) name: the hospital name
          (int) capacity: the capacity (the number of patients 
                          that can be accepted) of this hospital
          (time) OpenTime: the time this hospital starts to operate
          (time) CloseTime: the time this hospital ends its operation
        """
        GPSPoint.__init__(self, lat, lng)
        self.name = name
        self.capacity = capacity
        self.OpenTime = OpenTime
        self.CloseTime = CloseTime

        # The linked list of patients
        self.patients = None

    def isOpen(self):
        """
        Check whether or not this hospital is open now

        Return:
          (boolean) True: if the current time is between the OpenTime and CloseTime
        """
        # Get the current time (system time)
        current = datetime.datetime.now().time()

        if OpenTime == CloseTime:
            # This hospital operates 24/7
            return True
        
        return current >= OpenTime and current <= CloseTime         


    def hasCapacity(self):
        """
        Return whether or not this hospital has at least one capacity so that
        it can take one more patient.

        Return:
          (boolean) True: if capacity > 0; False: otherwise
        """
        return self.capacity > 0


    def receivePatient(self, patient):
        """
        Receive one patient and then add this patient to the patients linked list.
        Substract one from the capacity.

        Args:
          (crash) patient: the patient sent to this hospital
        """
        # Add this patient to self.patients linked list
        if self.patients == None:
            self.patients = patient
        else:
            pointer = self.patients.getTail()
            pointer.next = patient

        # Reduce the capacity by 1
        self.capacity -= 1






