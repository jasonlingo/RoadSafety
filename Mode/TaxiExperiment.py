import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import OUTPUT_DIRECTORY
from random import uniform 
from GPS.GPSPoint import GPSPoint
from Util.kml import KmzParser
from Map.MapMatrix import MapMatrix
from Google.Direction import getDirection
from Entity.Taxi import Taxi
from Entity.Crash import Crash
from Entity.Hospital import Hospital
from File.Directory import createDirectory
from time import sleep
import pygmaps
import webbrowser


class TaxiExperiment:
    """
    When a crash happens, find the taxi that can arrive the 
    crash location with minimal time among all the taxis in 
    the region.
    """
    ### Instance variable ###
    # (Taxi) the location of all taxis
    taxis = None
    # (Crash) the location of car creahes 
    crashes = None
    # (GPSPoint) list of hospital
    hospitals = None
    # Send-to-hospital record
    sendHistory = []


    def __init__(self, region_filename):
        """
        Construct an experiment

        Args:
          (String) region_filename: the location of the region 
                   file from Google MAP kmz file
        """
        # (GPSPoint) the GPS data of the region
        self.region = KmzParser(region_filename)
        
        # The map matrix used to store useful information
        self.Map = MapMatrix(self.region)


    def addHospital(self, hospital_filename):
        """
        Add hospitals' locations in the region

        Args:
          (String) hospital_filename: the locations of hospitals
                   to be added into the map
        """
        # Parse the hospitals' GPS data
        self.hospitals = KmzParser(hospital_filename)
        
        pointer = self.hospitals
        while pointer != None:
            # Find the sub-area that contains the GPS location of this hospital
            area = self.Map.findArea(pointer)
            # Add this hospital to the area
            hos = Hospital(pointer.lat, pointer.lng)
            area.addHospital(hos)
            # Next hospital
            pointer = pointer.next


    def addTaxi(self, taxis_filename):
        """
        Add taxis according to the given locations.
        
        Args:
          (String) taxis_filename: the location of a list of all 
                   the taxis in the region
        """
        # Parse the locations of taxis stored in a kmz file
        newTaxis = KmzParser(taxis_filename)
        
        # Add each taxi to its area
        pointer = newTaxis
        while pointer != None:
            # Find the sub-area that contains the GPS location of this taxi
            area = self.Map.findArea(pointer)
            # Create a taxi object
            taxi = Taxi(pointer.lat, pointer.lng, self.hospitals) # remove the hospital
            # Add this taxi to the area
            area.addTaxi(taxi)
            # Next taxi 
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
          (int) num: the number of taxis to add.
        """
        if self.taxis != None:
            # If this region already has taxis, append the new taxi 
            # to the tail of the taxi list.
            pointer = self.taxis.getTail()

        while num > 0:
            # Randomly create taxi's location
            lat = uniform(self.Map.bottom, self.Map.top)
            lng = uniform(self.Map.left, self.Map.right)
            
            taxiGPS = GPSPoint(lat, lng)
            # Get nearest road's GPS of that random location
            # taxiGPS = getRoadGPS(taxiGPS)
            
            # Check whether the taxi's GPS location is in the region
            if self.Map.isInnerPoint(taxiGPS):
                num -= 1;
                # Find the sub-area that contains the GPS location of this taxi
                area = self.Map.findArea(taxiGPS)
                # Create two identical taxi objects in order to prevent "pass by reference"
                taxi = Taxi(taxiGPS.lat, taxiGPS.lng, self.hospitals)
                taxi2 = Taxi(taxiGPS.lat, taxiGPS.lng, self.hospitals) 
                taxi.next = None
                area.addTaxi(taxi)
                
                # Add this taxi to the taxis linked list
                if self.taxis == None:
                    self.taxis = taxi2
                    pointer = self.taxis
                else:
                    pointer.next = taxi2
                    pointer = pointer.next

    def addCrash(self, crash_filename):
        """
        Add crashes according to the given location.
        
        Args:
          (String) crash_filename: the location of a list of all 
                   the crashes in the region
        """
        # Parse the locations of crashes stored in a kmz file
        newCrashes = KmzParser(crash_filename)

        # Add each crash to its area
        pointer = self.crashes
        while pointer != None:
            # Find the sub-area that contains the GPS location of this crash
            area = self.Map.findArea(pointer)
            # Create a single crash object
            crash = Crash(pointer.lat, pointer.lng, self.hospitals)
            # Add this crash to this area
            area.addCrash(crash)
            # Next crash
            pointer = pointer.next  

        if self.crashes != None:
            # There already are crashes in this experiment region, so attach the new crashes
            # to the tail of the crashes linked list
            pointer = self.crashes.getTail()
            pointer.next = newCrashes
        else:
            # There is no taxi in thie experiemnt region, so just replace the linked list
            self.taxis = newCrashes      


    def addRandomCrash(self, num):
        """
        Add taxis at random location in the region.

        Args:
          (int) num: the number of taxis to add.
        """        
        if self.crashes != None:
            pointer = self.crashes.getTail()

        while num > 0:
            # Create random crash's location
            lat = uniform(self.Map.bottom, self.Map.top)
            lng = uniform(self.Map.left, self.Map.right)
            
            crashGPS = GPSPoint(lat, lng)
            # Get nearest road's GPS of that random location
            #crashGPS = getRoadGPS(crashGPS)
            
            #check whether the taxi's GPS is in the region
            if self.Map.isInnerPoint(crashGPS):
                num -= 1;
                # Find the sub-area that contains the GPS location of this crash
                area = self.Map.findArea(crashGPS)
                # Create two identical taxi objects in order to prevent "pass by reference"
                crash = Crash(crashGPS.lat, crashGPS.lng, self.hospitals)
                crash2 = Crash(crashGPS.lat, crashGPS.lng, self.hospitals)
                crash.next = None
                area.addCrash(crash)

                # Add this crash to the crashes linked list
                if self.crashes ==  None:
                    self.crashes = crash2
                    pointer = self.crashes
                else:
                    pointer.next = crash2
                    pointer = pointer.next

    def sendPatients(self):
        """
        Send every patient to hospitals
        """
        if self.crashes == None:
            # No patient
            return

        self.crashes.printNode()
        pointer = self.crashes
        while pointer != None:
            self.sendToHospital(pointer)
            pointer = pointer.next

    def sendToHospital(self, crash):
        """send people to hospital from the crash location using Taxi.
        
        Args:
          (Crash) crash: the crash event
        """
        area = self.Map.findArea(crash)
        if area == None:
            print "This crash has a wrong location!!"
            return None
        row = area.row
        col = area.col
        print "A crash happened in area[%d, %d]" % (row, col)
        maxRow = len(self.Map.areas)
        maxCol = len(self.Map.areas[0])
        # Checking ranges
        if row > maxRow or col > maxCol:
            print "This crash has a wrong location!!"
            return None
        
        # Start to check from current location and its 8 neighbor sub-areas, 
        # and expand the range until a taxi or hospital is found.
        # When four flags (reachTop, reachBottom, reachRight, reachLeft) 
        # are all True, stop the checking process.
        reachTop    = False
        reachBottom = False
        reachRight  = False
        reachLeft   = False
        foundTaxi   = False
        shortestTime = float("inf")
        nearestTaxi = None
        nearestDirection = None
        # The duration between this crash to the nearest hospital

        destination = str(crash.lat) + "," + str(crash.lng)
        i = 0
        while not (reachTop and reachBottom and reachRight and reachLeft):
            for j in xrange(row - i, row + i + 1): 
                for k in xrange(col - i, col + i + 1):
                    if abs(row - j) < i and abs(col - k) < i:
                        # Already checked
                        continue

                    if self.Map.hasTaxi(j,k):
                        # Get the taxis linked list of this sub-area
                        taxi = self.Map.areas[j][k].taxis
                        while taxi != None:
                            if taxi.isEmpty:
                                foundTaxi = True
                                # Get a direction from the taxi's location to 
                                # the crash's location using Google Direciton API.
                                source = str(taxi.lat) + "," + str(taxi.lng)
                                direction = getDirection(source, destination)
                                duration = direction.getTotalDuration()
                                if duration < shortestTime:
                                    # Fine the taxi with shortest traffic time
                                    shortestTime = duration
                                    nearestTaxi = taxi
                                    nearestDirection = direction
                            taxi = taxi.next
            
            if foundTaxi and i > 0:
                # Mark this taxi as non-empty
                nearestTaxi.isEmpty = False
                # Update the taxi's GPS location
                nearestTaxi.lat = crash.lat
                nearestTaxi.lng = crash.lng
                # Market this patient as saved
                crash.isSaved = True
                # Make this taxi to find the nearest hospital and 
                # get the direction. 
                minute, second = nearestDirection.getDurationMS()
                print "The time for a nearest taxi to arrive this crash's location is "\
                      "%dmins %dsec" % (minute, second)
                
                HospitalDirection = nearestTaxi.toNearestHospital()
                minute, second = HospitalDirection.getDurationMS()
                print "Sending this patient to the nearest hospital needs------------ "\
                      "%dmins %dsec" % (minute, second)
                
                tail = nearestDirection.getTail()
                tail.next = HospitalDirection
                minute, second = nearestDirection.getDurationMS()
                print "Total time---------------------------------------------------- "\
                      "%dmins %dsec" % (minute, second)
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
        Show the experiment on Google map, including hospitals, 
        taxis, crashes, and taxis' route.
        """
        # Set the middle point of this map
        midLat = (self.Map.top + self.Map.bottom) / 2.0
        midLng = (self.Map.left + self.Map.right) / 2.0
        mymap = pygmaps.maps(midLat, midLng, 10)    
        
        # Add region line
        mymap.addpath(self.region.toList(), "#FF0000") #red

        # Add rectangle lines
        rectangle = [(self.Map.top, self.Map.left), 
                     (self.Map.top, self.Map.right),
                     (self.Map.bottom, self.Map.right),
                     (self.Map.bottom, self.Map.left),
                     (self.Map.top, self.Map.left)]
        mymap.addpath(rectangle, "#000000") #black  

        # Get the length of the side of each area
        latDiff = self.Map.latDiff    
        lngDiff = self.Map.lngDiff    
        
        # Add vertical lines
        lng = self.Map.left
        while lng <= self.Map.right: # From left to right
            line = [(self.Map.top, lng),
                    (self.Map.bottom, lng)]
            mymap.addpath(line, "#000000") #black             
            lng += lngDiff

        # Add last vertical line, using the residual length
        if lng - lngDiff < self.Map.right:
            line = [(self.Map.top, self.Map.right),
                    (self.Map.bottom, self.Map.right)]
            mymap.addpath(line, "#000000") #black 

        # Add horizontal lines
        lat = self.Map.top
        while lat >= self.Map.bottom: # From top to bottom
            line = [(lat, self.Map.left),
                    (lat, self.Map.right)]
            mymap.addpath(line, "#000000") #black
            lat -= latDiff  

        # Add last horizontal line, using the residual length
        if lat + latDiff > self.Map.bottom:
            line = [(self.Map.bottom, self.Map.left),
                    (self.Map.bottom, self.Map.right)]
            mymap.addpath(line, "#000000") #black             

        # Add taxis' locations
        pointer = self.taxis
        while pointer != None:
            mymap.addpoint(pointer.lat, pointer.lng, "#0000FF") #blue
            pointer = pointer.next

        # Add crashes' locations
        pointer = self.crashes
        while pointer != None:
            mymap.addpoint(pointer.lat, pointer.lng, "#00FF00") #green
            pointer = pointer.next

        # Add hospitals' locations
        pointer = self.hospitals
        while pointer != None:
            mymap.addpoint(pointer.lat, pointer.lng, "#FF0000") #green
            pointer = pointer.next

        # Add taxi routes:
        totalDuration = 0
        if len(self.sendHistory) > 0:
            for direction in self.sendHistory:
                mymap.addpath(direction.toList(), "#0000FF")
                totalDuration += direction.getTotalDuration()
        
        # Calculate average total time
        i = len(self.sendHistory)
        if i > 0:
            avgDuration = totalDuration / i
            sec = avgDuration % 60
            mins = (avgDuration - sec) / 60
            print "Average time: %dmins %dsec" % (mins, sec)

        # The output directory
        output_directory = OUTPUT_DIRECTORY + "Taxi_based_EMS/"   
        # Check whether the output directory exists. If not, create the directory
        createDirectory(output_directory)  
        # The file name of the result map   
        mapFilename = output_directory + "map.html"
        # Create the map
        mymap.draw('./'+mapFilename)
        
        # Open the file on a web browser
        url = "file://" + os.getcwd() + "/" + mapFilename
        webbrowser.open_new(url)

