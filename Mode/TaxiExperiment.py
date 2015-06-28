import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from parameter import OUTPUT_DIRECTORY
from random import uniform 
from GPXdata import GPSPoint
from Util.kml import KmzParser
from Map.haversine import haversine
from Map.RegionMap import RegionMap
from Map.MapMatrix import MapMatrix
from Google.Road import getRoadGPS
from GoogleStreetView import getDirection
from Entity.Taxi import Taxi
from Entity.Crash import Crash
from time import sleep
import pygmaps
import webbrowser
import thread


class TaxiExperiment:
    """
    When a crash happens, find the taxi that can arrive the 
    crash location with minimal time among all the taxis in 
    the region.
    """
    #map object
    #Map = None
    #MapMatrix = None
    #(GPSPoint) the GPS data of the region
    #region = None
    #(Taxi) the location of all taxis
    taxis = None
    #(Crash) the location of car creahes 
    crashes = None
    #(GPSPoint) list of hospital
    hospitals = None

    #send-to-hospital record
    sendHistory = []
    
    #rectangle 
    #top = 0
    #bottom = 0
    #right = 0
    #left = 0


    def __init__(self, region_filename):
        """
        Construct the experiment

        Args:
          (String) region_filename: the location of the region 
                   file from Google MAP kmz file
        """
        #(GPSPoint) the GPS data of the region
        self.region = KmzParser(region_filename)
        #RegionMap object
        self.Map = RegionMap(self.region)
        #rectangle of this map
        self.top = self.Map.top
        self.bottom = self.Map.bottom
        self.right = self.Map.right
        self.left = self.Map.left
        #the map matrix storing useful information
        self.MapMatrix = MapMatrix(self.top, self.bottom, self.right, self.left)


    def addHospital(self, hospital_filename):
        """
        Add hospitals' locations in the region

        Args:
          (String) hospital_filename: the locations of hospitals
                   to be added into the map
        """
        self.hospitals = KmzParser(hospital_filename)
        
        pointer = self.hospitals
        while pointer != None:
            area = self.MapMatrix.findArea(pointer)
            #print "add Hospital: Area[%d, %d]" %(area.row, area.col)
            hos = GPSPoint(pointer.lat, pointer.lng)
            area.addHospital(hos)
            pointer = pointer.next


    def addTaxi(self, taxis_filename):
        """
        Add taxis according to the given location.
        
        Args:
          (String) taxis_filename: the location of a list of all 
                   the taxis in the region
        """
        self.taxis = KmzParser(taxis_filename)
        pointer = self.taxis
        while pointer != None:
            area = self.MapMatrix.findArea(pointer)
            taxi = Taxi(pointer.lat, pointer.lng, self.hospitals)
            area.addHospital(taxi)
            pointer = pointer.next            


    def addRandomTaxi(self, num):
        """
        Add taxis at random location in the region.

        Args:
          (int) num: the number of taxis to add.
        """
        if self.taxis != None:
            pointer = self.taxis.getTail()

        while num > 0:
            #create random taxi's location
            lat = uniform(self.Map.bottom, self.Map.top)
            lng = uniform(self.Map.left, self.Map.right)
            
            #get nearest road's GPS of that random location
            taxiGPS = GPSPoint(lat, lng)
            #taxiGPS = getRoadGPS(taxiGPS)
            
            #check whether the taxi's GPS is in the region
            if self.Map.isInnerPoint(taxiGPS):
                #print "add a texi"
                num -= 1;
                area = self.MapMatrix.findArea(taxiGPS)
                taxi = Taxi(taxiGPS.lat, taxiGPS.lng, self.hospitals)
                taxi2 = Taxi(taxiGPS.lat, taxiGPS.lng, self.hospitals) #be careful of "pass by reference"
                taxi.next = None
                #print "add taxi: Area[%d, %d]" % (area.row, area.col)
                area.addTaxi(taxi)
                
                if self.taxis == None:
                    self.taxis = taxi2
                    pointer = self.taxis
                else:
                    pointer.next = taxi2
                    pointer = pointer.next
            #sleep(0.1)



    def addCrash(self, crash_filename):
        """
        Add crashes according to the given location.
        
        Args:
          (String) crash_filename: the location of a list of all 
                   the crashes in the region
        """
        self.crashes = KmzParser(crash_filename)
        pointer = self.crashes
        while pointer != None:
            area = self.MapMatrix.findArea(pointer)
            crash = Crash(pointer.lat, pointer.lng, self.hospitals)
            area.addCrash(crash)
            pointer = pointer.next  


    def addRandomCrash(self, num):
        """
        Add taxis at random location in the region.

        Args:
          (int) num: the number of taxis to add.
        """        
        if self.crashes != None:
            pointer = self.crashes.getTail()

        while num > 0:
            #create random taxi's location
            lat = uniform(self.Map.bottom, self.Map.top)
            lng = uniform(self.Map.left, self.Map.right)
            
            #get nearest road's GPS of that random location
            crashGPS = GPSPoint(lat, lng)
            #assume the accident not exactly happens on the road, 
            #it can be in a building (not car crash)
            #crashGPS = getRoadGPS(crashGPS)
            
            #check whether the taxi's GPS is in the region
            if self.Map.isInnerPoint(crashGPS):
                num -= 1;
                area = self.MapMatrix.findArea(crashGPS)
                crash = Crash(crashGPS.lat, crashGPS.lng, self.hospitals)
                crash2 = Crash(crashGPS.lat, crashGPS.lng, self.hospitals)
                #print "add crash: Area[%d, %d]" % (area.row, area.col)
                area.addCrash(crash)
                if self.crashes ==  None:
                    self.crashes = crash2
                    pointer = self.crashes
                else:
                    pointer.next = crash2
                    pointer = pointer.next

                self.sendToHospital(crash2)



    def sendToHospital(self, crash):
        """send people to hospital from the crash location using Taxi.
        
        Args:
          (Crash) crash: the crash event
        """
        GPS = GPSPoint(crash.lat, crash.lng)
        area = self.MapMatrix.findArea(GPS)
        row = area.row
        col = area.col
        print "a crash happened in area[%d, %d]" % (row, col)
        maxRow = len(self.MapMatrix.areas)
        maxCol = len(self.MapMatrix.areas[0])
        sleep(2)
        #checking range
        i = 0
        #check starts from current location and expand the range
        #when four flags are all True, stop checking
        reachTop    = False
        reachBottom = False
        reachRight  = False
        reachLeft   = False
        shortestTime = float("inf")
        foundTaxi = False
        nearestTaxi = None
        nearestDirection = None
        #the duration between this crash to the nearest hospital

        destination = str(crash.lat) + "," + str(crash.lng)
        while not (reachTop and reachBottom and reachRight and reachLeft):
            for j in xrange(row-i, row+i+1): 
                for k in xrange(col-i, col+i+1):
                    if abs(row-j) < i and abs(col-k) < i:
                        #already checked
                        continue
                    #print "checking area[%d, %d]" % (j, k) 
                    if self.MapMatrix.hasTaxi(j,k):
                        foundTaxi = True
                        taxi = self.MapMatrix.areas[j][k].taxis
                        while taxi != None:
                            if taxi.isEmpty:
                                source = str(taxi.lat) + "," + str(taxi.lng)
                                direction = getDirection(source, destination)
                                duration = direction.getTotalDuration()
                                if duration < shortestTime:
                                    shortestTime = duration
                                    nearestTaxi = taxi
                                    nearestDirection = direction
                            taxi = taxi.next
            if foundTaxi and i > 0:
                nearestTaxi.isEmpty = False
                nearestTaxi.lat = crash.lat
                nearestTaxi.lng = crash.lng
                crash.isSaved = True
                HospitalDirection = nearestTaxi.toNearestHospital()
                tail = nearestDirection.getTail()
                tail.next = HospitalDirection
                self.sendHistory.append(nearestDirection)
                break

            i += 1
            if reachBottom == False and row + i >= maxRow:
                reachBottom = True
            if reachTop == False and row - i < 0:
                reachTop = True
            if reachRight == False and col + i >= maxCol:
                reachRight = True
            if reachLeft == False and col - i < 0:
                reachLeft = True

        totalSecond = nearestDirection.getTotalDuration()
        second = totalSecond % 60
        minute = (totalSecond - second)/60
        print "sending people to hospital needs %dmins %dsec" % (minute, second)

    def showMap(self):
        """
        Show the experiment on Google map, including hospitals, 
        taxis, and crashes
        """
        midLat = (self.Map.top + self.Map.bottom)/2.0
        midLng = (self.Map.left + self.Map.right)/2.0
        #set the middle point of this map
        mymap = pygmaps.maps(midLat, midLng, 10)    
        #add region line
        mymap.addpath(self.region.toList(), "#FF0000") #red

        #add rectangle lines
        rectangle = [(self.top, self.left), 
                     (self.top, self.right),
                     (self.bottom, self.right),
                     (self.bottom, self.left),
                     (self.top, self.left)]
        mymap.addpath(rectangle, "#000000") #black  

        #get the length of the side of each area
        latDiff = self.MapMatrix.latDiff    
        lngDiff = self.MapMatrix.lngDiff    
        #add vertical lines
        lng = self.left
        while lng <= self.right:
            line = [(self.top, lng),
                    (self.bottom, lng)]
            mymap.addpath(line, "#000000") #black             
            lng += lngDiff
        #add last vertical line
        if lng - lngDiff < self.right:
            line = [(self.top, self.right),
                    (self.bottom, self.right)]
            mymap.addpath(line, "#000000") #black 

        #add horizontal lines
        lat = self.top
        while lat >= self.bottom:
            line = [(lat, self.left),
                    (lat, self.right)]
            mymap.addpath(line, "#000000") #black
            lat -= latDiff        
        #add last horizontal line
        if lat + latDiff > self.bottom:
            line = [(self.bottom, self.left),
                    (self.bottom, self.right)]
            mymap.addpath(line, "#000000") #black             

        #add taxis
        if self.taxis != None:
            for taxi in self.taxis.toList():
                mymap.addpoint(taxi[0], taxi[1], "#0000FF") #blue

        #add crashes
        if self.crashes != None:
            for crash in self.crashes.toList():
                mymap.addpoint(crash[0], crash[1], "#00FF00") #green

        #add hospitals
        if self.hospitals != None:
            for hospital in self.hospitals.toList():
                mymap.addpoint(hospital[0], hospital[1], "#FF0000") #red

        #add taxi routes:
        i = 0
        totalDuration = 0
        if len(self.sendHistory) > 0:
            for direction in self.sendHistory:
                i += 1
                mymap.addpath(direction.toList(), "#0000FF")
                totalDuration += direction.getTotalDuration()
                #direction = getRoadGPS(direction)
                #mymap.addpath(direction.toList(), "#0038ff")
        if i > 0:
            avgDuration = totalDuration/i
            sec = avgDuration % 60
            mins = (avgDuration - sec)/60
            print "Average time: %dmins %dsec" % (mins, sec)


        
        mapFilename = OUTPUT_DIRECTORY + "map.html"
        mymap.draw('./'+mapFilename)
        #sample: "file:///Users/Jason/GitHub/RoadSeftey/RoadSafety/map.html"
        url = "file://" + os.getcwd() + "/" + mapFilename
        webbrowser.open_new(url)

