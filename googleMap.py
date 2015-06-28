import os
import pygmaps 
import webbrowser
import googlemaps
from parameter import OUTPUT_DIRECTORY, GRID_DISTANCE
from datetime import datetime, date, time
from GPXdata import GPSPoint, haversine
from shapely.geometry import LineString

"""
gmaps = googlemaps.Client(key='AIzaSyCeDV3O8B3PJjRF3GYACJr7RNIa_WvJcsM')

# Geocoding and address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)
print directions_result
"""

def containPoint(region, checkPoint):
    """ 
    Check whether the region contains the point

    Args:
      (list) region: a list of GPS points of a region
      (GPSPoint) checkPoint: a point to be checked
    Return:
      (boolean) True if the region contains the point; False otherwise
    """
    #1. Find the highest point on the region line and add 0.001 to its latitude,
    #   then the new point must be a point outside the region.
    #2. Connect the new point with the checkPoint,
    #   check whether the line across the region line segmentation,
    #3. If the line across the region line for odd times, then the point is in the region

    #find the highest poin
    highest = region[0]
    for point in region:
        if point[0] > highest[0]:
            highest = point
    highest = (highest[0]+0.001, highest[1])
    intersectNum = 0
    pre = region[0]
    for point in region[1:]:
        line1 = LineString([(pre[0], pre[1]), (point[0], point[1])])
        line2 = LineString([(highest[0], highest[1]), (checkPoint.lat, checkPoint.lng)])
        if str(line1.intersection(line2)) != "GEOMETRYCOLLECTION EMPTY":
            intersectNum += 1
        pre = point

    return intersectNum%2 == 1





def showPath(path, framePoint, outputDirectory):
    """show GPS path on Google map"""
    #@parameter {list} path: a list of GPS data of a path
    #@parameter {list} framePoint: a list of GPS data of extracted video frames
    mymap = pygmaps.maps(path[0][0], path[0][1], 14)    
    newPath = list(path)
    mymap.addpath(newPath, "#FF0000")
    firstPoint = True
    for point in framePoint:
        if firstPoint:
            mymap.addpoint(point[0], point[1], "#00FF00")
            firstPoint = False
        else:
            mymap.addpoint(point[0], point[1], "#0000FF")
    mapFilename = outputDirectory + "map.html"
    mymap.draw('./'+mapFilename)
    #sample: "file:///Users/Jason/GitHub/RoadSeftey/RoadSafety/map.html"
    url = "file://" + os.getcwd() + "/" + mapFilename
    webbrowser.open_new(url)


def findInnerGrid(region, recTopRight=None, recTopLeft=None, recBotRight=None, recBotLeft=None):
    """
    find the inner grid within a region

    Args:
      (list) region: a list of GPS data of a region
      (GPSPoint) recTopRight, recTopLeft, recBotRight, recBotLeft:
                 the four corners of a rectangle that contains the region           
    Return:
      (list) gridPoint: a list of GPSPoints that are within the region
    """ 
   
    #add grids
    #find the distance (km) of two sides
    width = haversine(recTopRight.lat, recTopRight.lng,
                      recTopLeft.lat, recTopLeft.lng)
    height = haversine(recTopRight.lat, recTopRight.lng,
                       recBotRight.lat, recBotRight.lng)
    
    #number of segmentations (segmentated every 10km)
    numWidth = int(width)/GRID_DISTANCE
    numHeight = int(height)/GRID_DISTANCE

    #vertical segmentation distance
    lngDiff = (recTopRight.lng - recTopLeft.lng)/numWidth #need to deal with divide by zero

    #horizontal segmentation distance 
    latDiff = (recTopRight.lat - recBotRight.lat)/numHeight

    #find grid point
    gridPoint = []
    lng = recTopLeft.lng
    while(lng <= recTopRight.lng*1.0001):
        lat = recBotRight.lat
        while(lat <= recTopRight.lat*1.0001):
            point = GPSPoint(lat, lng)
            if containPoint(region, point):
                #if the region contains the point
                gridPoint.append(point)
            lat += latDiff
        lng += lngDiff

    return gridPoint


def showGrig(region, recTopRight, recTopLeft, recBotRight, recBotLeft, gridPoint, longestTimeDirection):
    """
    show region with grid points on Google map and 
    the direction with longest duration

    Args:
      (list) region: a list of GPS data of a region
      (GPSPoint) recTopRight, recTopLeft, recBotRight, recBotLeft:
                 the four corners of a rectangle that contains the region
      (list) gridPoint: the points within the region
      (linked list/GPSPoint) longestTimeDirection: the direction with longest duration           
    """

    #set middle point
    midLat = (recTopRight.lat + recBotLeft.lat)/2.0
    midLng = (recTopRight.lng + recBotLeft.lng)/2.0
    mymap = pygmaps.maps(midLat, midLng, 10)    
    
    #create the path for the rectangle
    rectangle = [(recTopRight.lat, recTopRight.lng),
                 (recTopLeft.lat, recTopLeft.lng),
                 (recBotLeft.lat, recBotLeft.lng),
                 (recBotRight.lat, recBotRight.lng),
                 (recTopRight.lat, recTopRight.lng)]    

    #add lines
    newRegion = list(region) #mymap.addpath() will add the "#FF0000" to the original list
    newRectangle = list(rectangle)
    mymap.addpath(newRegion, "#FF0000")
    mymap.addpath(newRectangle, "#0000FF")

    #add grids
    #find the distance (km) of two sides
    width = haversine(recTopRight.lat, recTopRight.lng,
                      recTopLeft.lat, recTopLeft.lng)
    height = haversine(recTopRight.lat, recTopRight.lng,
                       recBotRight.lat, recBotRight.lng)
    
    #number of segmentations (segmentated every 10km)
    numWidth = int(width)/GRID_DISTANCE
    numHeight = int(height)/GRID_DISTANCE

    #add vertical lines
    lngDiff = (recTopRight.lng - recTopLeft.lng)/numWidth
    lng = recTopLeft.lng + lngDiff
    while (lng < recTopRight.lng):
        line  = [(recTopRight.lat, lng),
                 (recBotRight.lat, lng)]
        mymap.addpath(line, "#0000FF")
        lng += lngDiff

    #add horizontal lines
    latDiff = (recTopRight.lat - recBotRight.lat)/numHeight
    lat = recBotRight.lat + latDiff
    while (lat < recTopRight.lat):
        line  = [(lat, recTopLeft.lng),
                 (lat, recTopRight.lng)]
        mymap.addpath(line, "#0000FF")
        lat += latDiff

    #add the direction with longest duration
    longestTimeDirectionList = longestTimeDirection.toList()
    mymap.addpath(longestTimeDirectionList, "#000000") #black
    
    #add grid points
    for point in gridPoint:
        mymap.addpoint(point.lat, point.lng, "#FF0000")

    mapFilename = OUTPUT_DIRECTORY + "mapGrid.html"
    mymap.draw('./'+mapFilename)
    #sample: "file:///Users/Jason/GitHub/RoadSeftey/RoadSafety/mapGrid.html"
    url = "file://" + os.getcwd() + "/" + mapFilename
    webbrowser.open_new(url)


