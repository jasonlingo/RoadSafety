import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Entity.Taxi import Taxi
from Entity.Crash import Crash
from GPS.GPSPoint import GPSPoint
from GPS.Haversine import Haversine
from config import GRID_DISTANCE
from shapely.geometry import LineString
from GPS.FindRectangleSideGPS import FindRectangleSideGPS



class MapMatrix():
    """
    A data structure for a map unit that contains lists of 
    hospitals, crashes, and taxis in the unit. A map unit 
    is obtained by dividing the map into several small squares.
    """

    def __init__(self, region, areaSize=GRID_DISTANCE):
        """
        Constructor

        Args:
          (GPSPoint) region: the GPS data of the given region
          (float) areaSize: the length of each side of sub-areas 
        """
        # Keep the region
        self.region = region

        # The matrix that stores the areas in thie MapMatrix
        self.areas = []
        
        # The border of this MapMatrix
        (self.top, self.bottom, self.right, self.left) = \
                            FindRectangleSideGPS(self.region)

        # For checking inner grid point
        self.CloseRegionList = region.toList()
        self.CloseRegionList.append((region.lat, region.lng))                            

        # The length of each side of areas in this MapMatrix
        self.areaSize = areaSize
        self.genSubAreas()

        # The GPS difference of width and height of each side of areas
        self.latDiff = 0
        self.lngDiff = 0

        # Generate the matrix for this map
        self.genSubAreas()


    def genSubAreas(self):
        """
        Generate sub-areas with each side length = areaSize in this map. 
        There might be some areas whose sides are small than areaSize.
        Each sub-area contains lists of taxis, hospitals and crashes.
        """
        # Calculate the width and height of this MapMatrix
        width = Haversine(self.top, self.left, self.top, self.right)
        height = Haversine(self.top, self.left, self.bottom, self.left)
        
        # Calculate the number of seqments of each side
        segmentW = float(width) / float(self.areaSize)
        segmentH = float(height) / float(self.areaSize)
        
        # Calculate the GPS difference between each segment
        self.latDiff = (self.top - self.bottom) / segmentH
        self.lngDiff = (self.right - self.left) / segmentW

        # Start generate areas
        # Row-major order matrix, index starts from 0
        row = 0 
        areaTop = self.top
        while areaTop > self.bottom: # From top to bottom
            # Insert a new row
            self.areas.append([])
            if areaTop - self.latDiff >= self.bottom:
                areaBot = areaTop - self.latDiff
            else:
                # Last area use the residual length
                areaBot = self.bottom
            
            # Index starts from 0
            col = 0 
            areaLeft = self.left
            while areaLeft < self.right: # From left to right
                if areaLeft + self.lngDiff <= self.right:
                    areaRight = areaLeft + self.lngDiff
                else:
                    # Last area use the residual length
                    areaRight = self.right
                # Insert this sub-area into the last row
                self.areas[-1].append(self.Area(areaTop, areaBot, areaRight, areaLeft, row, col))
                areaLeft = areaRight
                col += 1
            areaTop = areaBot
            row += 1


    def isInnerPoint(self, checkPoint):
        """ 
        Check whether the region contains the checkPoint
        #1. Find a point outside the region
        #2. Connect the new point with the checkPoint, then
        #   check whether the line across the region line segmentation
        #3. If the line across the region line for odd times, then the point is inside the region        

        Args:
          (GPSPoint) checkPoint: a point to be checked
        Return:
          (boolean) True if the region contains the point; False otherwise
        """
        ### Find a point outside the region ###
        highest = (self.top * 1.0001, self.right * 1.0001)
       
        # Initialize the number of intersection of the region line and 
        # the line that connects the outside point and the checkPoint.
        intersectNum = 0

        # The line connects the ckeckPoint and outside point
        line1 = LineString([(highest[0], highest[1]), (checkPoint.lat, checkPoint.lng)])         
        
        # Start counting the times of the line intersects the region lines
        pre = self.CloseRegionList[0]
        for point in self.CloseRegionList[1:]:
            # Region line (border)
            line2 = LineString([(pre[0], pre[1]), (point[0], point[1])]) 
            if str(line1.intersection(line2)) != "GEOMETRYCOLLECTION EMPTY":
                # Has an intersection with this regino line (border)
                intersectNum += 1
            pre = point

        return intersectNum % 2 == 1


    def hasTaxi(self, row, col):
        """
        Check whether the area containing the GPS location has a Taxi.

        Args:
          (int) row, col: the matrix indices 
        Return:
          (boolean) True if the area has at least one available Taxi.
        """
        if row < 0 or row >= len(self.areas) or col < 0 or col >= len(self.areas[0]):
            # Wrong indices
            print "Wrong indices!!"
            return False 

        area = self.areas[row][col]
        if area.taxis == None:
            return False
        else:
            taxi = area.taxis
            while taxi != None:
                if taxi.isEmpty == True:
                    return True
                taxi = taxi.next
        return False


    def findArea(self, GPS):
        """
        Find the area that contains the GPS location

        Args:
          (GPSPoint) GPS: the location we want to find its area
        """
        if (GPS.lat > self.top or GPS.lat < self.bottom or 
            GPS.lng < self.left or GPS.lng > self.right):
            # The GPS is not even in the whole MapMatrix
            print "Wrong GPS location!!"
            return None

        widthNum = int((GPS.lng - self.left) / self.lngDiff)
        heightNum = int((self.top - GPS.lat) / self.latDiff)

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
        """The sub-area in the matrix"""

        def __init__(self, top, bottom, right, left, row, col):
            """Constructor"""
            # The broders of this area
            self.top    = top
            self.bottom = bottom
            self.right  = right 
            self.left   = left
            
            # Matrix indices
            self.row = row
            self.col = col

            # The lists of hospitals, taxis, crashes in this sub-area.
            self.hospitals = None
            self.taxis     = None
            self.crashes   = None             

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


