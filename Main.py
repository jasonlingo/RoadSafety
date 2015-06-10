#!/usr/bin/env python
import sys
import datetime
import parameter
from Image import getVideoFrame
from GPXdata import parseGPX
from FileUtil import getFilename
from kml import KmzParser
from GoogleStreetView import getStreetView, LinkedListToList, getDirection
from GoogleMap import showPath

import pygmaps 
import webbrowser


def main():
    """
    Get street view images associated with GPS data

    mode:
      1. use video and recorded GPS data 
      2. use Google MAP kmz file
      3. use addresses
    """
    mode = 2



    if mode == 1:
        """
        Splitting videos into shorter videos and mapping GPS data to each shorter videos.
        """
        #get the video file name list in a given directory
        videos = getFilename(parameter.VIDEO_DIRECTORY, parameter.VIDEO_TYPE)
        #load GPX data in a given directory
        GPXs = getFilename(parameter.GPS_DIRECTORY, parameter.GPS_TYPE)
        gpsData = []
        for GPX in GPXs:
            gpsData += parseGPX(parameter.GPS_DIRECTORY + GPX)
        gpsData = sorted(gpsData)

        #check whether or not resize image
        if parameter.RESIZE_X == 1920:
            resize = False
        else:
            resize = True

        #get video frames according to the GPS distance
        for video in videos:
            getVideoFrame(gpsData, parameter.VIDEO_DIRECTORY + video, parameter.FLIP_IMAGE, resize)
            break


    elif mode == 2:
        """
        1. Input addresses for start and end points, 
        2. Get direction from Google MAP API, 
        3. Extrace GPS data from direction,
        4. Get and store street view images according to GPS and bearing,
        5. Show path and street view points on Google map.
        """
        #get detail GPS point list and linked list
        path, head = KmzParser("GPS/direction.kmz")
        head.printNode()
        #street view point
        SVPoint = getStreetView(head, parameter.VIDEO_FRAME_DIRECTORY+"mode2/")
        showPath(path, SVPoint)


    elif mode == 3:
        """

        """
        originAdd = raw_input("Please enter the address of starting point: ")
        destAdd = raw_input("Please enter destination address: ")
        #get direction
        direction = getDirection(originAdd, destAdd)
        #street view point
        SVPoint = getStreetView(direction, parameter.VIDEO_FRAME_DIRECTORY+"mode3/")
        #get GPS list from GPS linked list
        path = LinkedListToList(direction)
        #show path and street view points on Google MAP
        showPath(path, SVPoint)

if __name__ == '__main__':
    main()
