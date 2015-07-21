import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pygmaps 
import webbrowser


def showPath(path, framePoint, outputDirectory):
    """
    Show GPS path and extracted street view images' locations on Google map.

    Args: 
      (list) path: a list of GPS data of a path.
      (list) framePoint: a list of GPS data of extracted video frames.
      (String) outputDirectory: the folder for storing this map file.
    """

    # Set the center of this map. Using the starting point of the 
    # path as the center of the map.
    mymap = pygmaps.maps(path[0][0], path[0][1], 14)    

    # Add path to this map and set its color to "#FF0000".
    mymap.addpath(path, "#FF0000")

    # Add every points in framePoint to this map.
    firstPoint = True
    for point in framePoint:
        if firstPoint:
            # Set the first point with color = "#00FF00".
            mymap.addpoint(point[0], point[1], "#00FF00")
            firstPoint = False
        else:
            # The color of other points is "#0000FF".
            mymap.addpoint(point[0], point[1], "#0000FF")
    
    # Create this map.
    mapFilename = outputDirectory + "map.html"
    mymap.draw('./' + mapFilename)
    
    # Create the local link to this map file.
    url = "file://" + os.getcwd() + "/" + mapFilename
    
    # Open this map on a browser
    webbrowser.open_new(url)