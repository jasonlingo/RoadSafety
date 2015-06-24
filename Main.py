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
from web_snapshot import getStreetViewByUrl
from GoogleAPI import calcGridTrafficTime
import optparse
import pygmaps 
import webbrowser
from Mode.TaxiExperiment import TaxiExperiment


def main():
    """
    Get street view images associated with GPS data

    mode:
      1. use video and recorded GPS data 
      2. use Google MAP kmz file
      3. use addresses
    """
    optparser = optparse.OptionParser()
    optparser.add_option("-m", "--mode", dest="mode", default="3", help="mode of getting Street view")
    (opts, _) = optparser.parse_args()


    if opts.mode == "1":
        """
        Splitting videos into shorter videos and mapping GPS data to each shorter videos.
        """
        print "Start getting street view by mode 1"
        
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
            getVideoFrame(gpsData, parameter.VIDEO_DIRECTORY + video, parameter.FLIP_IMAGE, resize, parameter.VIDEO_FRAME_DIRECTORY+"mode1/")
            break


    elif opts.mode == "2":
        """
        1. Get route from KMZ file
        2. Get street view image using Google street view API
        3. Upload images to Google Drive
        4. Output a csv file that contains image names, image links, and GPS data,
        5. Show path and street view points on Google map
        """
        print "Start getting street view by mode 2"

        #get detail GPS point list and linked list
        head = KmzParser("GPS/Bangkok.kmz")
        #street view point
        SVPoint = getStreetView(head, parameter.VIDEO_FRAME_DIRECTORY+"mode2/")
        showPath(head.toList(), SVPoint)


    elif opts.mode == "3":
        """
        1. Input addresses for start and end points, 
        2. Get direction from Google MAP API, 
        3. Extrace GPS data from direction,
        4. Get and store street view images according to GPS and bearing,
        5. Show path and street view points on Google map.
        """
        print "Start getting street view by mode 3"

        originAdd = raw_input("Please enter the address of starting point: ")
        destAdd = raw_input("Please enter destination address: ")
        if not (originAdd == None or originAdd == "" or destAdd == None or destAdd == ""):
            #get direction
            direction = getDirection(originAdd, destAdd)
            direction.printNode()
            #street view point
            SVPoint = getStreetView(direction, parameter.VIDEO_FRAME_DIRECTORY+"mode3/")
            #get GPS list from GPS linked list
            path = LinkedListToList(direction)
            #show path and street view points on Google MAP
            showPath(path, SVPoint)
    

    elif opts.mode == "4":
        """
        1. Get route from KMZ file
        2. Get street view image using Google street view url
        3. Upload images to Google Drive
        4. Output a csv file that contains image names, image links, and GPS data,
        5. Show path and street view points on Google map,      
        """
        print "Start getting street view by mode 4"

        #get detail GPS point list and linked list
        head = KmzParser("GPS/Bangkok.kmz")
        head.printNode()
        #street view point
        SVPoint = getStreetViewByUrl(head, parameter.VIDEO_FRAME_DIRECTORY+"mode4/")
        showPath(head.toList, SVPoint)        


    elif opts.mode == "5":
        """
        Divide the given region into grid and calculate 
        point to point traffic itme.
        """
        head = KmzParser("GPS/Delhi.kmz")
        calcGridTrafficTime(head)


    elif opts.mode == "6":
        """
        TaxiExperiment: 
        When a crash happens, find the taxi that can arrive the 
        crash location with minimal time among all the taxis in 
        the region.        
        """
        ex = TaxiExperiment("GPS_data/Delhi.kmz")
        ex.addTaxi("GPS_data/Taxi.kmz")
        ex.addRandomTaxi(50)



if __name__ == '__main__':
    main()
