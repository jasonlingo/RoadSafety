import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import OUTPUT_DIRECTORY
from Util.kml import KmzParser
from Map.MapMatrix import MapMatrix
from Google.Direction import getDirection
from Google.Road import getRoadGPS
from Entity.Taxi import Taxi
from Entity.Crash import Crash
from Entity.Hospital import Hospital
from GPS.GPSPoint import GPSPoint
from File.Directory import createDirectory
from random import uniform 
from time import sleep
import pygmaps
import webbrowser


class TaxiExperiment:
    """
    This program is for Taxi-based EMS experiment.

    When a crash happens, this system will find the taxi that 
    can arrive the crash's location with the shortest time 
    among all the taxis in the region. Then, the taxi will 
    send the patient from the crash's location to the nearest
    hospital. 
    This system will record the traffic time for all patients 
    to be sent to a hospital and calculate the average traffic 
    time.
    """

    ### Instance variable ###
    # (Taxi) the location of all taxis.
    taxis = None
    # (Crash) the location of car creahes .
    crashes = None
    # (GPSPoint) list of hospital.
    hospitals = None
    # Send-to-hospital record, for average traffic time use.
    sendHistory = []


    def __init__(self, region_filename):
        """
        Construct an experiment.

        Args:
          (String) region_filename: the location of the region 
                   file from Google MAP kmz file
        """
        # Parse a the region stored in a kmz file and get its GPS data stored
        # in GPSPoint linked list.
        self.region = KmzParser(region_filename)
        
        # Create a MapMatrix used to store useful information for this experiment.
        self.Map = MapMatrix(self.region)


    def addHospital(self, hospital_filename):
        """
        Add hospitals' locations to this region.

        Args:
          (String) hospital_filename: the locations of hospitals
                   to be added into the map
        """
        # Parse the hospitals' GPS location from a kmz file and get their GPS 
        # linked list (GPSPoint).
        self.hospitals = KmzParser(hospital_filename)
        
        pointer = self.hospitals
        while pointer != None:
            # Find the sub-area that contains the GPS location of this hospital.
            area = self.Map.findArea(pointer)
            # Create a hospital object.
            hos = Hospital(pointer.lat, pointer.lng)
            # Add this hospital to the area.
            area.addHospital(hos)
            # Next hospital.
            pointer = pointer.next


    def addTaxi(self, taxis_filename):
        """
        Add taxis according to the given locations.
        
        Args:
          (String) taxis_filename: the location of a list of all 
                   the taxis in the region
        """
        # Parse the locations of taxis stored in a kmz file and get their GPS
        # location in a linked list (GPSPoint).
        newTaxis = KmzParser(taxis_filename)
        
        # Add each taxi to its area
        pointer = newTaxis
        while pointer != None:
            # Find the sub-area that contains the GPS location of this taxi.
            area = self.Map.findArea(pointer)
            # Create a taxi object.
            taxi = Taxi(pointer.lat, pointer.lng, self.hospitals) # remove the hospital
            # Add this taxi to the area.
            area.addTaxi(taxi)
            # Next taxi.
            pointer = pointer.next 

        if self.taxis != None:
            # There already are taxis in this experiment region, so attach the new taxis
            # to the tail of the taxis linked list
            pointer = self.taxis.getTail()
            pointer.next = newTaxis 
        else:
            # There is no taxi in thie experiemnt region, so just replace the linked list
            self.taxis = newTaxis          


    def addRandomTaxi(self, num):
        """
        Add taxis at random location in the region.

        Args:
          (int) num: the number of taxis to be added.
        """
        if self.taxis != None:
            # If this region already has taxis, append the new taxi 
            # to the tail of the taxi list.
            pointer = self.taxis.getTail()

        while num > 0:
            # Randomly create taxi's location.
            # uniform(a, b) will gererate a number between a and b in 
            # a uniform distribution manner.
            lat = uniform(self.Map.bottom, self.Map.top)
            lng = uniform(self.Map.left, self.Map.right)
            
            # create the taxi's GPS point.
            taxiGPS = GPSPoint(lat, lng)

            # Sometimes the genreated location is not on a road.
            # If we want the location to be on a road, perform 
            # getRoadGPS() to get nearest road's GPS to that random 
            # location.
            taxiGPS = getRoadGPS(taxiGPS)
            
            # Check whether the taxi's GPS location is in the region.
            # If the location is in the region, then add this taxi to 
            # this experiment.
            if self.Map.isInnerPoint(taxiGPS):
                num -= 1;
                # Find the sub-area that contains the GPS location of this taxi.
                area = self.Map.findArea(taxiGPS)
                # Create two identical taxi objects in order to prevent "pass by reference".
                taxi = Taxi(taxiGPS.lat, taxiGPS.lng, self.hospitals)
                taxi2 = Taxi(taxiGPS.lat, taxiGPS.lng, self.hospitals) 
                taxi.next = None
                area.addTaxi(taxi)
                
                # Add this taxi to the taxis linked list.
                if self.taxis == None:
                    self.taxis = taxi2
                    pointer = self.taxis
                else:
                    pointer.next = taxi2
                    pointer = pointer.next

    def addCrash(self, crash_filename):
        """
        Add crashes according to the given locations.
        
        Args:
          (String) crash_filename: the file stores the locations 
                   of crashes.
        """
        # Parse the locations of crashes stored in a kmz file, and get 
        # their GPS data in a linked list (GPSPoint).
        newCrashes = KmzParser(crash_filename)

        # Add each crash to its area.
        pointer = self.crashes
        while pointer != None:
            # Find the sub-area that contains the GPS location of this crash.
            area = self.Map.findArea(pointer)
            # Create a crash object.
            crash = Crash(pointer.lat, pointer.lng, self.hospitals)
            # Add this crash to this area.
            area.addCrash(crash)
            # Next crash.
            pointer = pointer.next  

        if self.crashes != None:
            # There already are crashes in this experiment region, so attach 
            # the new crashes to the tail of the crashes linked list.
            pointer = self.crashes.getTail()
            pointer.next = newCrashes
        else:
            # There is no taxi in thie experiemnt region, so just replace 
            # the linked list.
            self.taxis = newCrashes      


    def addRandomCrash(self, num):
        """
        Add taxis at random locations in the region.

        Args:
          (int) num: the number of taxis to add.
        """        
        if self.crashes != None:
            pointer = self.crashes.getTail()

        while num > 0:
            # Create random crash's location
            lat = uniform(self.Map.bottom, self.Map.top)
            lng = uniform(self.Map.left, self.Map.right)
            
            # Create the crash's GPS point.
            crashGPS = GPSPoint(lat, lng)

            # Sometimes the genreated location is not on a road.
            # If we want the location to be on a road, perform 
            # getRoadGPS() to get nearest road's GPS to that random 
            # location.
            #crashGPS = getRoadGPS(crashGPS)
            
            # Check whether the taxi's GPS is in the region.
            # If the location is in the region, then add this crash to 
            # this experiment.            
            if self.Map.isInnerPoint(crashGPS):
                num -= 1;
                # Find the sub-area that contains the GPS location of this crash.
                area = self.Map.findArea(crashGPS)
                # Create two identical taxi objects in order to prevent "pass by reference".
                crash = Crash(crashGPS.lat, crashGPS.lng, self.hospitals)
                crash2 = Crash(crashGPS.lat, crashGPS.lng, self.hospitals)
                crash.next = None
                area.addCrash(crash)

                # Add this crash to the crashes linked list.
                if self.crashes ==  None:
                    self.crashes = crash2
                    pointer = self.crashes
                else:
                    pointer.next = crash2
                    pointer = pointer.next

    def sendPatients(self):
        """
        Send every patient to hospitals.
        """
        if self.crashes == None:
            # No patient
            return
        # Print every patient's location on screen.
        self.crashes.printNode()

        pointer = self.crashes
        while pointer != None:
            # Send every patient to the nearest hospital.
            self.sendToHospital(pointer)
            pointer = pointer.next

    def sendToHospital(self, crash):
        """
        Send people to hospital from the crash's location by a Taxi.
        
        Args:
          (Crash) crash: the crash event.
        """
        # Find the sub-area that contains this crash.
        area = self.Map.findArea(crash)
        if area == None:
            # The system cannot find a sub-area that contains this crash.
            print "This crash has a wrong location!!"
            return
        
        # Get the row and column number of the found area.
        row = area.row
        col = area.col
        print "A crash happened in area[%d, %d]" % (row, col)
        
        # The maximal number of row and column of this MapMatrix.
        maxRow = len(self.Map.areas)
        maxCol = len(self.Map.areas[0])
        
        # Check ranges. If the row and column number are larger than the 
        # maximal row and column number of this mapMatrix, then stop this 
        # process.
        if row > maxRow or col > maxCol:
            print "This crash has a wrong location!!"
            return
        
        # Start to check from current location and its 8 neighbor sub-areas, 
        # a 3x3 grids centered at the current location, and expand the range 
        # until a taxi or hospital is found.
        # When four flags (reachTop, reachBottom, reachRight, reachLeft) 
        # are all True, stop the checking process because all the grids have 
        # already been checked.
        reachTop    = False
        reachBottom = False
        reachRight  = False
        reachLeft   = False

        # The data set for tracking the nearest taxi.
        foundTaxi   = False
        shortestTime = float("inf")
        nearestTaxi = None
        nearestDirection = None

        # The GPS string (lat,lng) of this crash. Used in getDirection().
        destination = str(crash.lat) + "," + str(crash.lng)
        
        # Start to find the nearest taxi.
        i = 0
        while not (reachTop and reachBottom and reachRight and reachLeft):
            for j in xrange(row - i, row + i + 1): 
                for k in xrange(col - i, col + i + 1):
                    if abs(row - j) < i and abs(col - k) < i:
                        # Those grids have already been checked, so skip to the next loop.
                        continue

                    if self.Map.hasTaxi(j,k):
                        # Get the taxis linked list of this sub-area.
                        taxi = self.Map.areas[j][k].taxis
                        while taxi != None:
                            if taxi.available:
                                # This taxi is available, so mark foundTaxi to True.
                                foundTaxi = True

                                # Get a direction from the taxi's location to 
                                # the crash's location using Google Direciton API.
                                source = str(taxi.lat) + "," + str(taxi.lng)
                                direction = getDirection(source, destination)
                                duration = direction.getTotalDuration()
                                if duration < shortestTime:
                                    # Update the nearest taxi's data.
                                    shortestTime = duration
                                    nearestTaxi = taxi
                                    nearestDirection = direction
                            taxi = taxi.next
            
            # If foundTaxi == True and i > 0, then we will assign the found taxi
            # to this crash. 
            # i must be larger than 0 because we want to check at least 9 grids 
            # centered at the crash's location.
            if foundTaxi and i > 0:
                # Mark this taxi as non-empty.
                nearestTaxi.available = False

                # Update the taxi's GPS location to the crash's location.
                nearestTaxi.lat = crash.lat
                nearestTaxi.lng = crash.lng

                # Market this patient as saved.
                crash.isSaved = True

                # Print the traffic time for the taxi to arrive the crash's 
                # location on screen.
                minute, second = nearestDirection.getDurationMS()
                print "The time for a nearest taxi to arrive this crash's location is "\
                      "%dmins %dsec" % (minute, second)
                
                # Make the taxi to find the nearest hospital by get and compare
                # the traffic time of each direction to different hospital.
                HospitalDirection = nearestTaxi.toNearestHospital()
                minute, second = HospitalDirection.getDurationMS()
                print "Sending this patient to the nearest hospital needs------------ "\
                      "%dmins %dsec" % (minute, second)
                
                # Concatenate the two directions so that it become a direction from the 
                # taxi's original location to the crash's then to the hospital's.
                tail = nearestDirection.getTail()
                tail.next = HospitalDirection

                # Get the total traffic time. 
                minute, second = nearestDirection.getDurationMS()
                print "Total time---------------------------------------------------- "\
                      "%dmins %dsec" % (minute, second)

                # Append this direction to the sendHistory list for calculating the 
                # average traffic time.      
                self.sendHistory.append(nearestDirection)
                break

            i += 1
            # Check whether any side of this region has been reached.
            if reachBottom == False and row + i >= maxRow:
                reachBottom = True
            if reachTop == False and row - i < 0:
                reachTop = True
            if reachRight == False and col + i >= maxCol:
                reachRight = True
            if reachLeft == False and col - i < 0:
                reachLeft = True

    def showMap(self):
        """
        Show the experiment result on Google map, including hospitals, 
        taxis, crashes, and taxis' route.
        """
        # Set the center point of this map.
        midLat = (self.Map.top + self.Map.bottom) / 2.0
        midLng = (self.Map.left + self.Map.right) / 2.0
        mymap = pygmaps.maps(midLat, midLng, 10)    
        
        # Add region line (border).
        mymap.addpath(self.region.toList(), "#FF0000") #red

        # Add rectangle lines.
        rectangle = [(self.Map.top, self.Map.left), 
                     (self.Map.top, self.Map.right),
                     (self.Map.bottom, self.Map.right),
                     (self.Map.bottom, self.Map.left),
                     (self.Map.top, self.Map.left)]
        mymap.addpath(rectangle, "#000000") #black  

        # Get the length of the side of each sub-area.
        latDiff = self.Map.latDiff    
        lngDiff = self.Map.lngDiff    
        
        # Add vertical lines.
        lng = self.Map.left
        while lng <= self.Map.right: # From left to right.
            line = [(self.Map.top, lng),
                    (self.Map.bottom, lng)]
            mymap.addpath(line, "#000000") #black             
            lng += lngDiff

        # Add last vertical line, using the residual length.
        if lng - lngDiff < self.Map.right:
            line = [(self.Map.top, self.Map.right),
                    (self.Map.bottom, self.Map.right)]
            mymap.addpath(line, "#000000") #black 

        # Add horizontal lines.
        lat = self.Map.top
        while lat >= self.Map.bottom: # From top to bottom.
            line = [(lat, self.Map.left),
                    (lat, self.Map.right)]
            mymap.addpath(line, "#000000") #black
            lat -= latDiff  

        # Add last horizontal line, using the residual length.
        if lat + latDiff > self.Map.bottom:
            line = [(self.Map.bottom, self.Map.left),
                    (self.Map.bottom, self.Map.right)]
            mymap.addpath(line, "#000000") #black             

        # Add taxis' locations.
        pointer = self.taxis
        while pointer != None:
            mymap.addpoint(pointer.lat, pointer.lng, "#0000FF") #blue
            pointer = pointer.next

        # Add crashes' locations.
        pointer = self.crashes
        while pointer != None:
            mymap.addpoint(pointer.lat, pointer.lng, "#00FF00") #green
            pointer = pointer.next

        # Add hospitals' locations.
        pointer = self.hospitals
        while pointer != None:
            mymap.addpoint(pointer.lat, pointer.lng, "#FF0000") #green
            pointer = pointer.next

        # Add taxi routes.
        totalDuration = 0
        if len(self.sendHistory) > 0:
            for direction in self.sendHistory:
                mymap.addpath(direction.toList(), "#0000FF") #blue
                totalDuration += direction.getTotalDuration()
        
        # Calculate average traffic time.
        i = len(self.sendHistory)
        if i > 0:
            avgDuration = totalDuration / i
            sec = avgDuration % 60
            mins = (avgDuration - sec) / 60
            print "Average traffic time: %dmins %dsec" % (mins, sec)

        # The output directory.
        output_directory = OUTPUT_DIRECTORY + "Taxi_based_EMS/"   

        # Check whether the output directory exists. If not, create the directory.
        createDirectory(output_directory)  

        # The file name of the result map. 
        mapFilename = output_directory + "map.html"
        
        # Draw the map.
        mymap.draw('./' + mapFilename)
        
        # Open the map file on a web browser.
        url = "file://" + os.getcwd() + "/" + mapFilename
        webbrowser.open_new(url)

