#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


#import datetime
import optparse
from File.getFilename import getFilename
from Video.getVideoFrame import getVideoFrame
from config import VIDEO_DIRECTORY, GPS_DIRECTORY, VIDEO_FRAME_DIRECTORY
from config import VIDEO_TYPE, GPS_TYPE, RESIZE_X, FLIP_IMAGE
from GPS.parseGPX import parseGPX
from Util.kml import KmzParser



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
        videos = getFilename(VIDEO_DIRECTORY, VIDEO_TYPE)
        #load GPX data in a given directory
        GPXs = getFilename(GPS_DIRECTORY, GPS_TYPE)
        gpsData = []
        for GPX in GPXs:
            gpsData += parseGPX(GPS_DIRECTORY + GPX)
        gpsData = sorted(gpsData)

        #check whether or not resize image, should modify this to compare the actual size, not pre-defined size
        if RESIZE_X == 1920:
            resize = False
        else:
            resize = True

        #get video frames according to the GPS distance
        for video in videos:
            getVideoFrame(gpsData, VIDEO_DIRECTORY + video, FLIP_IMAGE, resize, VIDEO_FRAME_DIRECTORY+"mode1/")
            break


    elif opts.mode == "2":
        """
        1. Get route from KMZ file
        2. Get street view image using Google street view API
        3. Upload images to Google Drive
        4. Output a csv file that contains image names, image links, and GPS data,
        5. Show path and street view points on Google map
        """
        from Google.StreetView import getStreetView
        from Google.showPath import showPath

        print "Start getting street view by mode 2"

        #get detail GPS point list and linked list
        head = KmzParser("GPS_data/Thailand_roads/Rattanathibet.kmz")
        #street view point
        outputDirectory = VIDEO_FRAME_DIRECTORY+"mode2/Rattanathibet/"
        SVPoint = getStreetView(head, outputDirectory)
        showPath(head.toList(), SVPoint, outputDirectory)


    elif opts.mode == "3":
        """
        1. Input addresses for start and end points, 
        2. Get direction from Google MAP API, 
        3. Extrace GPS data from direction,
        4. Get and store street view images according to GPS and bearing,
        5. Show path and street view points on Google map.
        """
        from Google.Direction import getDirection
        from Google.StreetView import getStreetView
        from Google.showPath import showPath
        print "Start getting street view by mode 3"

        originAdd = raw_input("Please enter the address of starting point: ")
        destAdd = raw_input("Please enter destination address: ")
        if not (originAdd == None or originAdd == "" or destAdd == None or destAdd == ""):
            #get direction
            direction = getDirection(originAdd, destAdd)
            direction.printNode()
            #street view point
            outputDirectory = VIDEO_FRAME_DIRECTORY+"mode3/"
            SVPoint = getStreetView(direction, outputDirectory)
            #get GPS list from GPS linked list
            path = direction.toList()
            #show path and street view points on Google MAP
            showPath(path, SVPoint, outputDirectory)
    

    elif opts.mode == "4":
        """
        1. Get route from KMZ file
        2. Get street view image using Google street view url
        3. Upload images to Google Drive
        4. Output a csv file that contains image names, image links, and GPS data,
        5. Show path and street view points on Google map,      
        """
        from Google.getStreetViewByUrl import getStreetViewByUrl
        from Google.showPath import showPath
        print "Start getting street view by mode 4"

        #get detail GPS point list and linked list
        head = KmzParser("GPS_data/Thailand_roads/Sukhumvit.kmz")
        head.printNode()
        #street view point
        outputDirectory = VIDEO_FRAME_DIRECTORY+"mode4/Sukhumvit/"
        SVPoint = getStreetViewByUrl(head, outputDirectory)
        showPath(head.toList(), SVPoint, outputDirectory)        


    elif opts.mode == "5":
        """
        Divide the given region into grid and calculate 
        point to point traffic itme.
        """
        from Google.GridTrafficTime import GridTrafficTime
        head = KmzParser("GPS_data/Delhi.kmz")
        GridTrafficTime(head)


    elif opts.mode == "6":
        """
        TaxiExperiment: 
        When a crash happens, find the taxi that can arrive the 
        crash location with minimal time among all the taxis in 
        the region.        
        """
        from Mode.TaxiExperiment import TaxiExperiment
        ex = TaxiExperiment("GPS_data/Delhi.kmz")
        #Hospitals must be added before adding taxis and crashes
        ex.addHospital("GPS_data/Hospital.kmz")
        #ex.addTaxi("GPS_data/Taxi.kmz")
        try:
            taxiNum = raw_input("How many taxis? ")
            taxiNum = int(taxiNum)
            print "The number of taxis is ", taxiNum
        except ValueError:
            print "The input format is wrong. We will use 50 taxis in this experiment."
            taxiNum = 50;
        ex.addRandomTaxi(taxiNum)
        #add crashes
        crashNum = 1
        while crashNum > 0:
            try:
                crashNum = int(raw_input("How many crashes do you want to add? "))
                ex.addRandomCrash(crashNum)
            except ValueError:
                print "Wrong format!"
        ex.showMap()
        #ex.MapMatrix.printArea()

    elif opts.mode == "7":
        """
        Get street view images of major roads in a region/city.
        """
        from Mode.GetCityStreetView import GetCityStreetView

        # initialize a GetCityStreetView 
        st = GetCityStreetView("GPS_data/Delhi.kmz")
        



if __name__ == '__main__':
    main()
