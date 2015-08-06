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
 
    options (-m + option):
    Road safety project:
    1. Get street view images from road videos. Extract video frames
       every certain distance according to GPS data. 
    
    2. Get street view images from Google street view API according to 
       a route created by "Google My MAP" service. 
    
    3. Get street view images from Google street view API according to 
       a direction from Google Direction API. 

    4. Get street view images from Google MAP street view on a web browser 
       according to a route created by "Google My MAP" service.

    5. Automatically find the roads in a region (or city) and 
       get their street view images from Google street view API.

    Taxi-based EMS project.
    a. Divide the given region into grids and calculate point-to-point 
       traffic time.

    b. Taxi-based EMS Simulation: 
       When a crash happens, find the taxi that can arrive the 
       crash's location with shortest time among all the taxis in 
       the region. Then send this patient from the crash's location 
       to a nearest hospital. Finally output the average time that a 
       patient is sent to a hospital.

    c. Snapshot Google MAP traffic periodically.
    """    
    optparser = optparse.OptionParser()
    optparser.add_option("-m", "--mode", dest="mode", default="1", help="mode of getting Street view")
    (opts, _) = optparser.parse_args()


    if opts.mode == "1":
        """
        Get street view images from road videos. Extract video frames
        every certain distance according to corresponding GPS data. 

        1. Parse GPS data.
        2. Extract video frames according to GPS data.
        3. Upload extracted images to Googld Drive.
        4. Output uploaded images' public link and their GPS data 
           to a csv file.
        5. Show the path and the locations of extracted images on 
           Google map.
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
        Get street view images from Google street view API according to 
        a route created by "Google My MAP" service. 
        
        1. Get route from a KMZ file.
        2. Get street view images using Google street view API.
        3. Upload images to Google Drive.
        4. Output uploaded images' public link and their GPS data 
           to a csv file.
        5. Show the path and the locations of street view images on 
           Google map.
        """
        from Google.StreetView import getStreetView
        from Google.showPath import showPath
        from File.Directory import createDirectory

        # Parse the kmz file and get a GPSPoing linked list.
        head = KmzParser("Data/Thailand_roads/Rattanathibet.kmz")
        
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
        Get street view images from Google street view API according to 
        a direction from Google Direction API. 
        
        1. Enter addresses for start and end points.
        2. Get direction using Google Directoin API.
        3. Extract street view images according to the direction route.
        4. Upload images to Google Drive.
        5. Output uploaded images' public link and their GPS data 
           to a csv file.
        6. Show the path and the locations of street view images on 
           Google map.
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
        Get street view images from Google MAP street view on a web browser 
        according to a route created by "Google My MAP" service.
        
        1. Get route from KMZ file
        2. Capture street view image using Google MAP street view on a web browser 
           according to the route.
        3. Upload images to Google Drive
        4. Output a csv file that contains image names, image links, and GPS data,
        5. Show path and street view points on Google map      
        """
        from Google.getStreetViewByUrl import getStreetViewByUrl
        from Google.showPath import showPath
        from File.Directory import createDirectory

        # Parse the kmz file and get a GPSPoing linked list.
        head = KmzParser("Data/Thailand_roads/Sukhumvit.kmz")

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
        Get street view images of roads in a region/city.

        Still working on thie function.
        """
        from Mode.GetRegionStreetView import GetRegionStreetView
        
        # Parse the kmz file and get a GPSPoing linked list.
        head = KmzParser("Data/Bangkok_region.kmz")

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
        head = KmzParser("Data/Delhi.kmz")
        
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
        ex = TaxiExperiment("Data/Delhi.kmz")

        # Hospitals must be added before adding taxis and crashes.
        ex.addHospital("Data/Hospital.kmz")

        # If you want to add taxis at pre-defined locations, use the command.
        ex.addTaxi("Data/Taxi.kmz")
        
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
        Snapshot Google MAP traffic periodically.
        """
        from Google.trafficSnapshot import trafficSnapshot
        from GPS.GPSPoint import GPSPoint

        # Set the center of this traffic map.
        center = GPSPoint(13.7246005,100.6331108)

        # Start capturing traffic images.
        trafficSnapshot(center, 5, 2, 12)



    elif opts.mode == "d":
        """
        A similar mode like mode b but add a function to 
        draw the result on a line chart.
        """
        from config import DATABASE_ADDRESS
        import sqlite3 as lite

        ###
        # Write a record for this experiment into the table
        # "Experiment" in the "taxi_ems.db".
        
        # Connect DB.
        conn = lite.connect(DATABASE_ADDRESS)
        c = conn.cursor()


        # Find the largest experiment id and add one to the number
        # to get the new experiment id.
        command1 = '''
        select id from Experiment 
        order by id desc
        limit 1
        '''

        # Quota for Google direciton API. 
        # apiQuota = 1930

        # Initial number of taxis.
        taxiNum = 50
        crashNum = 3 # should modify this to automatically get the number

        while taxiNum <= 50:
            c.execute(command1)
            result = c.fetchone()
            if result == None or result == ():
                exId = 1
            else:
                exId = result[0] + 1

            print "Experiment No.%2d -----------------------------" % exId

            totHospital, avgTransferTime = TaxiProcess(taxiNum, crashNum, exId)

            # Write a new record for this experiment.
            # values (id, num_of_taxi, num_of_hospital, num_of_crash, 
            #         avg_taxi_arrival_time, avg_to_hospital_time)
            command2 = '''
            insert into Experiment values (%d, %d, %d, %d, 0, 0, %d)
            ''' % (exId, taxiNum, totHospital, crashNum, avgTransferTime + 480)
            c.execute(command2)
            conn.commit()

            taxiNum += 50 

        conn.close()



def TaxiProcess(taxiNum, crashNum, exId):
    from Mode.TaxiExperiment2 import TaxiExperiment2

    # Create an experiment object of the given region.
    ex = TaxiExperiment2("Data/Delhi.kmz", exId)

    # Hospitals must be added before adding taxis and crashes.
    ex.addHospital("Data/Hospital.kmz")

    # Add taxi's hot spots.
    ex.addTaxiHotSpot("Data/Taxi_hotspot.kmz")

    # Generate taxis at random locations.
    ex.addWeightedRandomTaxi(taxiNum)

    # Total number of hospitals.
    totHospital = ex.hospitals.nodeNum()

    # Add random crashes.
    #ex.addRandomCrash(crashNum)
    #ex.addCrash('Data/Crashes.kmz')

    # Send patients from the crash locations to hospitals.
    ex.sendPatients()

    # Show the result.
    avgTransferTime = int(ex.showMap())

    #ex.clearSelf()

    return totHospital, avgTransferTime



if __name__ == '__main__':
    main()
