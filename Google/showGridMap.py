import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pygmaps 
import webbrowser
from config import OUTPUT_DIRECTORY, GRID_DISTANCE
from datetime import datetime, date, time
from GPS.GPSPoint import GPSPoint 
from GPS.Haversine import Haversine



def showGridMap(region, recTopRight, recTopLeft, recBotRight, recBotLeft, gridPoint, longestTimeDirection):
    """
    Show the region with grid points and the direction with longest 
    duration on Google map 

    Args:
      (list) region: a list of GPS data of a region
      (GPSPoint) recTopRight, recTopLeft, recBotRight, recBotLeft:
                 the four corners of a rectangle that contains the region
      (list) gridPoint: the points within the region
      (GPSPoint) longestTimeDirection: the direction with longest duration           
    """

    # Set the middle point of the final map.
    midLat = (recTopRight.lat + recBotLeft.lat) / 2.0
    midLng = (recTopRight.lng + recBotLeft.lng) / 2.0
    mymap = pygmaps.maps(midLat, midLng, 10)    
    
    # Create the path (four sides) for the rectangle.
    rectangle = [(recTopRight.lat, recTopRight.lng),
                 (recTopLeft.lat, recTopLeft.lng),
                 (recBotLeft.lat, recBotLeft.lng),
                 (recBotRight.lat, recBotRight.lng),
                 (recTopRight.lat, recTopRight.lng)]    

    # Add region and rectangle lines
    newRegion = list(region) 
    newRectangle = list(rectangle)
    mymap.addpath(newRegion, "#FF0000")
    mymap.addpath(newRectangle, "#0000FF")

    # Add grids.
    # Find the distance (km) of two sides.
    width = Haversine(recTopRight.lat, recTopRight.lng,
                      recTopLeft.lat, recTopLeft.lng)
    height = Haversine(recTopRight.lat, recTopRight.lng,
                       recBotRight.lat, recBotRight.lng)
    
    # Number of segmentations (segmentated every 10km).
    numWidth = int(width)/GRID_DISTANCE
    numHeight = int(height)/GRID_DISTANCE

    # Add vertical lines to the map.
    lngDiff = (recTopRight.lng - recTopLeft.lng) / numWidth
    lng = recTopLeft.lng + lngDiff
    while (lng < recTopRight.lng):
        line  = [(recTopRight.lat, lng),
                 (recBotRight.lat, lng)]
        mymap.addpath(line, "#0000FF")
        lng += lngDiff

    # Add horizontal lines to the map.
    latDiff = (recTopRight.lat - recBotRight.lat) / numHeight
    lat = recBotRight.lat + latDiff
    while (lat < recTopRight.lat):
        line  = [(lat, recTopLeft.lng),
                 (lat, recTopRight.lng)]
        mymap.addpath(line, "#0000FF")
        lat += latDiff

    # Add the direction with the longest duration to the map.
    longestTimeDirectionList = longestTimeDirection.toList()
    mymap.addpath(longestTimeDirectionList, "#000000") #black
    
    # Add grid points to the map.
    for point in gridPoint:
        mymap.addpoint(point.lat, point.lng, "#FF0000")

    # Draw the map.
    mapFilename = OUTPUT_DIRECTORY + "mapGrid.html"
    mymap.draw('./' + mapFilename)

    # Open this map on a web browser.
    url = "file://" + os.getcwd() + "/" + mapFilename
    webbrowser.open_new(url)