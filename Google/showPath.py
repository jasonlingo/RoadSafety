import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pygmaps 
import webbrowser
import googlemaps
from config import OUTPUT_DIRECTORY, GRID_DISTANCE


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