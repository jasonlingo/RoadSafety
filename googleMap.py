import os
import pygmaps 
import webbrowser
import googlemaps
from datetime import datetime, date, time

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


def showPath(path, framePoint):
    """show GPS path on Google map"""
    #@parameter {list} path: a list of GPS data of a path
    #@parameter {list} framePoint: a list of GPS data of extracted video frames
    mymap = pygmaps.maps(path[0][0], path[0][1], 14)    
    mymap.addpath(path, "#FF0000")
    for point in framePoint:
        mymap.addpoint(point[0], point[1], "#0000FF")
    mapFilename = "map.html"
    mymap.draw('./'+mapFilename)
    #sample: "file:///Users/Jason/GitHub/RoadSeftey/RoadSafety/map.html"
    url = "file://" + os.getcwd() + "/" + mapFilename
    webbrowser.open_new(url)