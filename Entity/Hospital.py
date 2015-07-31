import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint

class Hospital(GPSPoint):

    def __init__(self, lat, lng, name="", capacity=10):
        """
        Construct a Hospital object.

        Args:
          (float) lat, lng: the GPS location of this Hospital.
          (String) name: the hospital name.
          (int) capacity: the capacity (the number of patients 
                          that can be accepted) of this hospital.
        """
        GPSPoint.__init__(self, lat, lng)

        # Initialize the properties of this hospital.
        self.name = name
        self.capacity = capacity

        # The patient list of this hospital.
        self.patients = None


    def hasCapacity(self):
        """
        Check whether this hospital has at least one capacity.

        Return:
          (boolean) True: if capacity > 0; False: otherwise.
        """
        return self.capacity > 0

    def acceptPatient(self, patient):
        """
        Accept one patient. Add this patient to the patient list 
        of this hospital and reduce the capacity by one.

        Args:
          (crash) patient: the patient who is sending to this hospital.
        Return:
          (boolean) True: if accept this patient successfully; 
                    False: otherwise.
        """
        if self.hasCapacity():
            # Has at least one capacity, so use one capacity of this hospital.
            self.capacity -= 1
            # Add this patient to the list.
            if self.patients == None:
                self.patients = patient
            else:
                pointer = self.patients.getTail()
                pointer.next = patient
            return True
        else:
            # Has no capacity.
            return False




