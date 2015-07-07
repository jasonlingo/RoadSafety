import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pygmaps 
import webbrowser
import googlemaps
from config import OUTPUT_DIRECTORY, GRID_DISTANCE
from datetime import datetime, date, time
from GPS.GPSPoint import GPSPoint 
from GPS.Haversine import Haversine
from shapely.geometry import LineString


def showGridMap(region, recTopRight, recTopLeft, recBotRight, recBotLeft, gridPoint, longestTimeDirection):
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
    width = Haversine(recTopRight.lat, recTopRight.lng,
                      recTopLeft.lat, recTopLeft.lng)
    height = Haversine(recTopRight.lat, recTopRight.lng,
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