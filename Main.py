# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import optparse
from config import VIDEO_FRAME_DIRECTORY
from Util.kml import KmzParser
from File.Directory import createDirectory

def main():
    """
    A starting point of each program for different experiments.
 
    opts (-m + option[1~5]):

    1. Get street view images from road videos. Extract video frames
       every certain distance according to GPS data. 
    
    2. Get street view images from Google street view API according to 
       a route created by "Google My MAP" service. 
    
    3. Get street view images from Google street view API according to 
       a direction from Google Direction API. 

    4. Get street view images from Google street view on a webbrowser 
       according to a route created by "Google My MAP" service.

    5. Automatically find the major roads in a region (or city) and 
       get their street view images from Google street view API.

    6. Divide the given region into grids and calculate point-to-point 
       traffic time.

    7. Taxi-based EMS Simulation: 
       When a crash happens, find the taxi that can arrive the 
       crash's location with shortest time among all the taxis in 
       the region. Then send this patient from the crash's location 
       to a nearest hospital.
    """    
    optparser = optparse.OptionParser()
    optparser.add_option("-m", "--mode", dest="mode", default="1", help="mode of getting Street view")
    (opts, _) = optparser.parse_args()


    if opts.mode == "1":
        """
        Get street view images from road videos. Extract video frames
        every certain distance according to corresponding GPS data. 
        """
        from config import VIDEO_DIRECTORY, GPS_DIRECTORY
        from config import VIDEO_TYPE, GPS_TYPE
        from config import RESIZE_X, FLIP_IMAGE
        from config import GPS_DISTANCE
        from Video.getVideoFrame import getVideoFrame
        from File.getFilename import getFilename
        from File.Directory import createDirectory
        from GPS.parseGPX import parseGPX

        # Get the video file name list in a given directory.
        videos = getFilename(VIDEO_DIRECTORY, VIDEO_TYPE)
        
        # Get the GPX file name list in a given directory.
        GPXs = getFilename(GPS_DIRECTORY, GPS_TYPE)

        # Parse all the GPS data and store them in a list.
        gpsData = []
        for GPX in GPXs:
            gpsData += parseGPX(GPS_DIRECTORY + GPX)
        # Sort GPS data by date and time.
        gpsData = sorted(gpsData)

        # Create the output folder if it doesn't exist.
        createDirectory(VIDEO_FRAME_DIRECTORY + "mode1/")

        # Get video frames according to the GPS distance.
        for video in videos:
            getVideoFrame( gpsData, 
                           VIDEO_DIRECTORY + video, 
                           FLIP_IMAGE, RESIZE_X, 
                           VIDEO_FRAME_DIRECTORY + "mode1/", 
                           GPS_DISTANCE )
            # Only process the first video, 
            # Should be able to process multiple videos
            break 


    elif opts.mode == "2":
        """
        1. Get route from a KMZ file.
        2. Get street view images using Google street view API.
        3. Upload images to Google Drive.
        4. Output a csv file that contains image names, image links, and GPS data.
        5. Show the path and street view images' locations on Google map.
        """
        from Google.StreetView import getStreetView
        from Google.showPath import showPath
        from File.Directory import createDirectory

        # Parse the kmz file and get a GPSPoing linked list.
        head = KmzParser("GPS_data/Thailand_roads/Rattanathibet.kmz")
        
        # Set the output folder.
        outputDirectory = VIDEO_FRAME_DIRECTORY + "mode2/Rattanathibet/"

        # Create the output folder if it doesn't exist
        createDirectory(outputDirectory)

        # Get street view images and get their corresponding locations.
        SVPoint = getStreetView(head, outputDirectory)

        # Show the path and street view images on a map.
        showPath(head.toList(), SVPoint, outputDirectory)


    elif opts.mode == "3":
        """
        1. Input addresses for start and end points.
        2. Get direction from Google MAP API.
        3. Extrace GPS data from direction.
        4. Get and store street view images according to GPS and bearing.
        5. Show path and street view points on Google map.
        """
        from Google.Direction import getDirection
        from Google.StreetView import getStreetView
        from Google.showPath import showPath
        from GPS.GPSPoint import GPSPoint
        from File.Directory import createDirectory

        # Get the source and destination addresses form user input.
        originAdd = raw_input("Please enter the address of starting point: ")
        destAdd = raw_input("Please enter destination address: ")

        if not (originAdd == None or originAdd == "" or destAdd == None or destAdd == ""):
            # Get direction from Google Direction API.
            direction = getDirection(originAdd, destAdd)

            # Print the direction data on screen.
            direction.printNode()

            # Set the output directory.
            outputDirectory = VIDEO_FRAME_DIRECTORY + "mode3/"
            
            # Create the output directory if it doesn't exist.
            createDirectory(outputDirectory)
            
            # Get Street view images.
            SVPoint = getStreetView(direction, outputDirectory)

            # Get GPS list from GPSPoint linked list.
            path = direction.toList()

            # Show path and street view points on Google MAP.
            showPath(path, SVPoint, outputDirectory)
        else:
            print "Please enter both addresses."
    

    elif opts.mode == "4":
        """
        1. Get route from KMZ file
        2. Get street view image using Google street view url
        3. Upload images to Google Drive
        4. Output a csv file that contains image names, image links, and GPS data,
        5. Show path and street view points on Google map      
        """
        from Google.getStreetViewByUrl import getStreetViewByUrl
        from Google.showPath import showPath
        from File.Directory import createDirectory

        # Parse the kmz file and get a GPSPoing linked list.
        head = KmzParser("GPS_data/Thailand_roads/Sukhumvit.kmz")

        # Print the GPS data on screen.
        head.printNode()

        # Set the output directory.
        outputDirectory = VIDEO_FRAME_DIRECTORY + "mode4/Sukhumvit/"

        # Create the output directory if it doesn't exist.
        createDirectory(outputDirectory)

        # Capture the street view images via web browser.
        SVPoint = getStreetViewByUrl(head, outputDirectory)

        # Show the path and the extraced street view images' locations.
        showPath(head.toList(), SVPoint, outputDirectory)        


    elif opts.mode == "5":
        """
        Get street view images of major roads in a region/city.
        """
        from Mode.GetRegionStreetView import GetRegionStreetView
        
        # Parse the kmz file and get a GPSPoing linked list.
        head = KmzParser("GPS_data/Delhi.kmz")

        # Create a GetRegionStreetView object.
        rsv = GetRegionStreetView(head)



    ##### Taxi-based EMS experiments #####

    elif opts.mode == "a":
        """
        Divide the given region into grids and get point-to-point traffic time
        using Google Direction API.
        """
        from Mode.GridTrafficTime import GridTrafficTime

        # Parse the kmz file and get a GPSPoing linked list of the region's border.
        head = KmzParser("GPS_data/Delhi.kmz")
        
        # Get the traffic time point-to-point in a grid map of the region.
        GridTrafficTime(head)


    elif opts.mode == "b":
        """
        Taxi-based EMS Simulation: 
        When a crash happens, find the taxi that can arrive the 
        crash location with minimal time among all the taxis in 
        the region.        
        """
        from Mode.TaxiExperiment import TaxiExperiment

        # Create an experiment object of the given region.
        ex = TaxiExperiment("GPS_data/Delhi.kmz")

        # Hospitals must be added before adding taxis and crashes.
        ex.addHospital("GPS_data/Hospital.kmz")

        # If you want to add taxis at pre-defined locations, use the command.
        ex.addTaxi("GPS_data/Taxi.kmz")
        
        # Ask the number of randomly generated taxis.
        try:
            taxiNum = raw_input("How many taxis? ")
            taxiNum = int(taxiNum)
        except ValueError:
            print "The input format is wrong. We will use 50"\
                  "taxis in this experiment."
            taxiNum = 50;

        # Generate taxis at random locations.
        ex.addRandomTaxi(taxiNum)

        totTaxi = ex.taxis.nodeNum()

        print "The total number of taxis is %d, including %d pre-defined taxis." \
                                 % (totTaxi, totTaxi - taxiNum) 

        # Add crashes to this experiment.
        # Ask the number of crashes that are going to be generated randomly.
        try:
            crashNum = int(raw_input("How many crashes do you want to add in this experiment? "))
            crashNum = int(crashNum)
            ex.addRandomCrash(crashNum)
        except ValueError:
            print "Wrong format!"
            sys.exit()

        # Send patients from the crash locations to hospitals.
        ex.sendPatients()

        # Show the result.
        ex.showMap()


    elif opts.mode == "c":
        """
        Capture Google traffic snapshot periodically
        """
        from Google.trafficSnapshot import trafficSnapshot
        from GPS.GPSPoint import GPSPoint

        center = GPSPoint(13.7246005,100.6331108)
        trafficSnapshot(center, 5, 2, 12)



if __name__ == '__main__':
    main()
