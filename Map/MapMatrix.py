import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Entity.Taxi import Taxi
from Entity.Crash import Crash
from GPXdata import GPSPoint
from Map.haversine import haversine
from parameter import GRID_DISTANCE



class MapMatrix():
    """
    A data structure for a map unit that contains lists of 
    hospitals, crashes, and taxis in the unit. A map unit 
    is obtained by dividing the map into several small squares.
    """
    #the border of this MapMatrix
    top    = None
    bottom = None
    right  = None
    left   = None
    #the length of each side of areas in this MapMatrix
    areaSize = 0
    #the GPS difference of width and height of each side of areas
    latDiff = 0
    lngDiff = 0
    #the matrix that stores the areas in thie MapMatrix
    areas = []

    def __init__(self, top, bottom, right, left, areaSize=GRID_DISTANCE):
        """
        Args:
          (float) top, bottom, right, left: the four borders 
                  of this MapMatrix
        """
        self.top    = top
        self.bottom = bottom
        self.right  = right
        self.left   = left
        self.areaSize = areaSize
        self.genAreas()
    

    def genAreas(self):
        """
        Generate areas with each side length = areaSize in this map
        """
        #calculate the width and height of the MapMatrix
        width = haversine(self.top, self.left, self.top, self.right)
        height = haversine(self.top, self.left, self.bottom, self.left)
        #calculate the number of seqments
        numWidth = float(width)/float(self.areaSize)
        numHeight = float(height)/float(self.areaSize)
        #calculate the GPS difference between each segment
        self.latDiff = (self.top - self.bottom)/numHeight
        self.lngDiff = (self.right - self.left)/numWidth

        #start generate areas
        row = 0
        areaTop = self.top
        while areaTop > self.bottom: #from top to bottom
            self.areas.append([])
            if areaTop - self.latDiff >= self.bottom:
                areaBot = areaTop - self.latDiff
            else:
                #last area use the residual space
                areaBot = self.bottom
            col = 0
            areaLeft = self.left
            while areaLeft < self.right: #from left to right
                if areaLeft + self.lngDiff <= self.right:
                    areaRight = areaLeft + self.lngDiff
                else:
                    #last area use the residual space
                    areaRight = self.right
                self.areas[-1].append(self.Area(areaTop, areaBot, areaRight, areaLeft, row, col))
                areaLeft = areaRight
                col += 1
            areaTop = areaBot
            row += 1


    def hasTaxi(self, row, col):
        """Check whether the area containing the GPS location has Taxi.

        Args:
          (int) row, col: the matrix indices 
        Return:
          (boolean) True if the area has at least one available Taxi.
        """
        if row < 0 or row >= len(self.areas) or col < 0 or col >= len(self.areas[0]):
            #wrong indices
            return False 

        area = self.areas[row][col]
        if area.taxis == None:
            return False
        else:
            pointer = area.taxis
            while pointer != None:
                if pointer.isEmpty == True:
                    return True
                pointer = pointer.next
        return False


    def findArea(self, GPS):
        """
        Find the area that contains the GPS location

        Args:
          (GPSPoint) GPS: the location we want to find its area
        """
        if (GPS.lat > self.top or GPS.lat < self.bottom or 
            GPS.lng < self.left or GPS.lng > self.right):
            #the GPS is not even in the whole MapMatrix
            return None

        widthNum = int((GPS.lng - self.left)/self.lngDiff)
        heightNum = int((self.top - GPS.lat)/self.latDiff)

        return self.areas[heightNum][widthNum]


    def printArea(self):
        """print all the info about a area"""
        for i in xrange(len(self.areas)):
            for j in xrange(len(self.areas[i])):
                print "Area[%d, %d]" % (i, j)
                area = self.areas[i][j]
                if area.hospitals != None:
                    print "Hospitals:"
                    area.hospitals.printNode()
                if area.taxis != None:
                    print "Taxis:"
                    area.taxis.printNode()
                if area.crashes != None:
                    print "Crashes:"
                    area.crashes.printNode()



    class Area():
        """The unit area in the matrix"""
        #the lists
        #(GPSPoint)
        hospitals = None
        #(Taxi)
        taxis = None
        #(Crash)
        crashes = None 

        def __init__(self, top, bottom, right, left, row, col):
            """Constructor"""
            #The broders of this area
            self.top = top
            self.bottom = bottom
            self.right = right 
            self.left = left
            #matrix indices
            self.row = row
            self.col = col


        def addHospital(self, hospitalList):
            """
            Add hospitals to this area

            Args:
              (GPSPoint) hospitalList: linked list of hospitals
            """
            if self.hospitals == None:
                self.hospitals = hospitalList
            else:
                tail = self.hospitals.getTail()
                tail.next = hospitalList

        def addTaxi(self, taxiList):
            """
            Add taxis to this area

            Args:
              (Taxi) taxiList: linked list of taxis
            """
            if self.taxis == None:
                self.taxis = taxiList
            else:
                tail = self.taxis.getTail()
                tail.next = taxiList

        def addCrash(self, crashList):
            """
            Add crashes to this area

            Args:
              (Crash) crashList: linked list of crashes
            """
            if self.crashes == None:
                self.crashes = crashList
            else:
                tail = self.crashes.getTail()
                tail.next = crashList

        def containsPoint(self, GPS):
            """
            Check whether this area contains the GPS point

            Args:
              (GPSPoint) GPS: the given GPS point to be checked
            Return:
              (boolean) True if the GPS point is in this MapMatrix;
                        False otherwise
            """
            if GPS.lng <= self.right and GPS.lng >= self.left and GPS.lat <= self.top and GPS.lat >= self.bottom:
                return True
            else:
                return False
