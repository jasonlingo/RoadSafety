import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from GPS.Distance import Haversine
from Google.Direction import getDirection
from Google.Road import getRoadGPS
from GPS.FindRectangleSideGPS import FindRectangleSideGPS
from config import OUTPUT_DIRECTORY
import pygmaps
import webbrowser
import os

class GridMap:
    """ 
    Create a grid map of a given region.
    """

    def __init__(self, region, gridSize):
        """
        Construct a grid map. 

        Args:
          (GPSPoint) region: a linked list of the GPS data of the
                     given region.
        """
        # Keep the region list.
        self.region = region

        # Keep the length of each size of a grid.
        self.gridSize = gridSize

        # Find top, bottom, right, left of a smallest rectangle
        # that contains the given region.
        (self.top, self.bottom, self.right, self.left) = \
                         FindRectangleSideGPS(self.region)

        # Initialize the grids matrix as an empty list.
        # This will store all the grid points of this grid map.
        self.grids = []

        # Initialize self.streetViewGPS list.
        self.streetViewGPS = []

        # Initialize source and destination list.
        self.SourceDestination = []

        # Initialize direction list.
        self.directions = []

        # Start generating grid points.
        self.genGrids()


    def genGrids(self):
        """
        Generate sub-areas with each side length = areaSize in this map. There 
        might be some areas whose sides are small than areaSize.
        """
        # Calculate the width and height of this MapMatrix.
        width = Haversine(self.top, self.left, self.top, self.right)
        height = Haversine(self.top, self.left, self.bottom, self.left)
        
        # Calculate the number of seqments of each side.
        segmentW = float(width) / float(self.gridSize)
        segmentH = float(height) / float(self.gridSize)
        
        # Calculate the difference in GPS between each segment.
        self.latDiff = (self.top - self.bottom) / segmentH
        self.lngDiff = (self.right - self.left) / segmentW

        # Start generating grid points.
        gridLat = self.top # From top to bottom.
        while gridLat >= self.bottom: 
            # Append a new empty row at the last of the matrix.
            self.grids.append([])    

            gridLng = self.left # From left to right.
            while gridLng <= self.right: 
                # Append the newly generated grid point into the last row.
                newGPS = getRoadGPS(GPSPoint(gridLat, gridLng))

                self.grids[-1].append(self.gridPoint(newGPS.lat, newGPS.lng))
                
                if gridLng != self.right and gridLng + self.lngDiff > self.right:
                    # The last longitude uses the residual length.
                    gridLng = self.right
                else:
                    gridLng += self.lngDiff

            if gridLat != self.bottom and gridLat - self.latDiff < self.bottom:
                # The last latitude uses the residual length.
                gridLat = self.bottom
            else:
                gridLat -= self.latDiff


    def getGridStreetView(self, outputDirectory):
        """
        Get the direction from a grid point located on the side of this 
        region to the grid point on the opposite side. Also add some middle
        point in the direction in order to prevent duplications of road 
        selection.
        """
        # Build the horizontal and vertical directions of this region.
        self.buildDirections()

        # Get directions using the source, destinatino, and waypoint data 
        # stored in self.directions. 
        self.queryDirection()

        # Find the GPS positions for this program to extract their street
        # view images.
        self.FindStreetViewGPS()


    def buildDirections(self):
        """
        Build vertical and horizontal directions, including intermediate points
        between every source and destination pairs.
        """
        if self.grids == []:
            # There is no grid point in the region.
            return

        # Initialize source and destination list.
        self.SourceDestination = []

        # Get the numbers of row and column.
        rowNum = len(self.grids)    
        colNum = len(self.grids[0])
        print "row: %d, col: %d" % (rowNum, colNum)

        # Use Google Direction and Road to produce all the 
        # GPS points that their street images are going to 
        # be extracted. Then make sure the GPS points will 
        # not duplicate with each other. 
        # Finally, use Google Street View API to get the 
        # street view images and upload them to Google Drive.
        
        # The maximum allowed waypoints is 8. So there will be 
        # 9 segmentations between every two consecutive grid points.
        MAX_SEGMENTATION = 9

        for i in xrange(colNum):
            for j in xrange(rowNum):
                # Get this source point.
                point = self.grids[j][i]

                # Write the GPS data of this source point in a string.
                source = str(point.lat) + "," + str(point.lng)

                # Build the query for the direction from this source point to 
                # its eastern grid point.
                if i + 1 < colNum: 
                    print "Build the query of direction from [%d, %d] to [%d, %d]" % (j, i, j, i + 1)
                    # Get the grid point at the east of this grid point.
                    EasternPoint = self.grids[j][i + 1]
                    
                    # Write the GPS data of this destination point of this direction in a string.
                    destination = str(EasternPoint.lat) + "," + str(EasternPoint.lng)
                    
                    # Calculate the difference in longitude between every two consecutive waypoints.
                    lngDiff = (EasternPoint.lng - point.lng) / MAX_SEGMENTATION
                    
                    for k in xrange(1, MAX_SEGMENTATION):# 0:source; 9:destination, 1~8:waypoints
                        if k == 1:
                            # The first waypoint.
                            waypoint = GPSPoint(point.lat, point.lng + lngDiff * k)
                            # Keep the head of this linked list.
                            waypointHead = waypoint
                        else:
                            waypoint.next = GPSPoint(point.lat, point.lng + lngDiff * k)
                            waypoint = waypoint.next
                    # Append this query of direction in the self.SourceDestination list.
                    self.SourceDestination.append(self.Direction(source, destination, waypointHead))


                # Build the query for the direction from this source point to 
                # its southern grid point. 
                if j + 1 < rowNum:
                    print "Build the query of direction from [%d, %d] to [%d, %d]" % (j, i, j + 1, i)
                    # Get the grid point at the south of this grid point.
                    SouthernPoint = self.grids[j + 1][i]

                    # Write the GPS data of this destination point of this direction in a string.
                    destination = str(SouthernPoint.lat) + "," + str(SouthernPoint.lng)
                    
                    # Calculate the difference in latitude between every two consecutive waypoints.
                    latDiff = (SouthernPoint.lat - point.lat) / MAX_SEGMENTATION
                    
                    for k in xrange(1, MAX_SEGMENTATION):# 0:source; 9:destination, 1~8:waypoints
                        if k == 1:
                            # The first waypoint.
                            waypoint = GPSPoint(point.lat + latDiff * k, point.lng)
                            # Keep the head of this linked list.
                            waypointHead = waypoint
                        else:
                            waypoint.next = GPSPoint(point.lat + latDiff * k, point.lng)
                            waypoint = waypoint.next
                    # Append this query of direction in the self.SourceDestination list.
                    self.SourceDestination.append(self.Direction(source, destination, waypointHead))                    




        """
        # Build vertical directions.
        for i in xrange(colNum):
            waypoint = None
            for j in xrange(rowNum):
                # self.grids[row][col]
                point = self.grids[j][i] 
                if j == 0:
                    # This is the source point.
                    # Write the GPS data of this first point in a string.
                    source = str(point.lat) + "," + str(point.lng)
                elif j == rowNum - 1:
                    # This is the destination point.
                    # Write the GPS data of this last point in a string.
                    destination = str(point.lat) + "," + str(point.lng)
                else:
                    # Those points are the intermediate points between the
                    # source and destination points. 
                    # Write those points as the waypoints.
                    if j == 1:
                        # Create the first intermediate point.
                        waypoint = GPSPoint(point.lat, point.lng)
                        waypointHead = waypoint
                    else:
                        waypoint.next = GPSPoint(point.lat, point.lng)
                        waypoint = waypoint.next
            self.SourceDestination.append(self.Direction(source, 
                                                         destination, 
                                                         waypointHead if waypoint != None
                                                         else None))


        # Build horizontal directions.
        for j in xrange(rowNum):
            waypoint = None
            for i in xrange(colNum):
                # self.grids[row][col]
                point = self.grids[j][i]
                if i == 0:
                    # This is the source point.
                    # Write the GPS data of this first point in a string.
                    source = str(point.lat) + "," + str(point.lng)
                elif i == colNum - 1:
                    # This is the destination point.
                    # Write the GPS data of this last point in a string.
                    destination = str(point.lat) + "," + str(point.lng)
                else:
                    # Those points are the intermediate points between the
                    # source and destination points. 
                    # Write those points as the waypoints.
                    if i == 1:
                        # Create the first intermediate point.
                        waypoint = GPSPoint(point.lat, point.lng)
                        waypointHead = waypoint
                    else:
                        waypoint.next = GPSPoint(point.lat, point.lng)
                        waypoint = waypoint.next
            self.SourceDestination.append(self.Direction(source, 
                                                         destination, 
                                                         waypointHead if waypoint != None
                                                         else None))        
        """

    def queryDirection(self):
        """
        Use the source, destination, and waypoint data to query directions 
        using Google Direction API.
        After got the directions from Google Direction API, use Google Road API
        to adjust the GPS position to a nearest road. 
        """
        # Initialize self.directions
        self.directions = []

        # for test
        midLat = (self.top + self.bottom) / 2 
        midlng = (self.right + self.left) / 2 
        mymap = pygmaps.maps(midLat, midlng, 10)
        rectangle = [(self.top, self.left), 
                     (self.top, self.right),
                     (self.bottom, self.right),
                     (self.bottom, self.left),
                     (self.top, self.left)]
        mymap.addpath(rectangle, "#000000") #black  


        # For every source and destination stored in self.SourceDestination list,
        # quey its direction using Google Direction API.
        print "The total number of query of direction is ", len(self.SourceDestination)
        con = raw_input("Do you want to continue? [y/n]: ")
        if con not in ["y", "Y"]:
            return
        
        i = 1
        for sd in self.SourceDestination:
            if i % 10 == 0:
                sys.stderr.write(".")
                sys.stderr.flush()


            # Get direction from Google Direction API
            direction = getDirection(sd.source, sd.destination, sd.waypoints)
            if direction != None:
                mymap.addpath(direction.toList(), "#FF0000")
                #direction.printNode()
                
                # Adjust the direciton to nearest roads.
                direction = getRoadGPS(direction)
                mymap.addpath(direction.toList(), "#0000FF") 
                #direction.printNode()

                # Append this adjusted direction to self.directions list.
                self.directions.append(direction)
            
            i += 1


        mapFilename = OUTPUT_DIRECTORY + "map.html"
        mymap.draw('./' + mapFilename)
        url = "file://" + os.getcwd() + "/" + mapFilename
        webbrowser.open_new(url)


    def FindStreetViewGPS(self):
        """
        For each direction stored in self.directions, find the GPS positions that 
        each of them has a certain distance away from its consecutive GPS positions.
        """
        # Initialize the list for storing GPS data for street images' location.
        GPSList = []
        for direction in self.directions:
            pass
            #direction.printNode()






    def showMap(self):  
        pass  



    class gridPoint:
        """
        The class for grid points.
        """

        def __init__(self, lat, lng):
            """Constructor"""
            # The GPS data of this grid point.
            self.lat = lat
            self.lng = lng


    class Direction:
        """
        A class that can store the source, destination and waypoints.
        """

        def __init__(self, source, destination, waypoints):
            """
            Construct a Direction object.

            Args:
              (String) source: the source point of this direction.
              (String) destination: the destination point of this direction.
              (GPSPoint)
            """
            self.source = source
            self.destination = destination
            self.waypoints = waypoints

    class StreetViewGPS:
        """
        A class that stores street view image's GPS location and 
        bearing.
        """

        def __init__(self, lat, lng, bearing):
            """
            Construct a StreetViewGPS object.

            Args:
              (float) lat, lng: the GPS data of this street view.
              (float) bearing: the compass bearing of this street view.
            """
            self.lat = lat
            self.lng = lng
            self.bearing = bearing


