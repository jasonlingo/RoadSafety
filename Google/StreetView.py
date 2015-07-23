import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import GPS_DISTANCE, FOLDER_NAME, API_KEY
from GPS.getBearing import getBearing
from Google.combineUrl import combineUrl
from Google.Drive import GDriveUpload
from File.outputCSV import outputCSV
from GPS.getIntermediatePoint import getIntermediatePoint
import urllib


def getStreetView(path, outputDirect):
    """
    1. Get street view from Google Street View API.
    2. Upload images to Google Drive.
    3. Output a csv file that contains image names, links to image, and GPS data.

    Args:
      (GPSPoint) path: a linked list of GPS point.
      (String) outputDirect: the directory for storing extracted images.
    Return:
      (list) Street view images' location data.
    """

    # The API url of the street view API
    STREET_API_URL = 'https://maps.googleapis.com/maps/api/streetview?'
    
    # The image number.
    imageNum = 1
    
    # Convert kilometer to meter.
    gps_distance_meter = GPS_DISTANCE * 1000
    
    # Street view points.
    SVPoint = []
    
    # Dataset for csv file.
    csvDataset = []
    GPSList = {}
    
    # For showing the progress.
    loop = 0
    while path.next != None:               
        # Show the progress on the command line screen. 
        # Make sure the process is still working.
        if loop % 10 == 0:
            sys.stderr.write(".")
            sys.stderr.flush()
        loop += 1
        

        distance = path.distance

        # Calculate how many segments in this path
        cutNum = int(round(distance / gps_distance_meter))

        if cutNum > 1:
            # This sub-path is too long, so cut it into several shorter pathes.
            gpsList = getIntermediatePoint(path, path.next, cutNum)
        elif cutNum == 0:
            # This sub-path is too short (less than 0.5 * gps_distance_meter), 
            # so find the next point that will make this total sub-path longer.
            start = path
            while path.next != None:
                if distance + path.next.distance < gps_distance_meter:
                    # Accumulate the distance.
                    distance += path.next.distance
                    path = path.next
                else:
                    # The new sub-path is already long enough, so stop this while loop.
                    break
            gpsList = [(start, path)]
        else:
            # This sub-path is longer than 0.5 * gps_distance_meter but 
            # less than 1.5 * gps_distance_meter. 
            # Just add one point to the list.
            gpsList = [(path, path.next)]

        # Get the street view images of the GPS points in gpsList using Google Street View API.
        for gps in gpsList:
            # Find the compass bearing of the two points.
            bearing = getBearing(gps[0], gps[1])
            
            # The parameters for Google Street View API.
            params = {
                # Image size; max=600x400.
                'size':'600x400', 
                # Horizontal field of view; max=120.
                'fov':'75',  
                # The up or down angle of the camera relative to the Street View vehicle;  
                # 90=sky, -90=floor, 0=front.    
                'pitch':'0',       
                # The compass bearing; 0~360; 0=North, 90=East, 180=South, 270=West.                  
                'heading':str(bearing), 
                # Current GPS point. 
                'location':str(gps[0].lat) + ',' + str(gps[0].lng),
                # Google API key
                'key':'AIzaSyCLP5d5vcwI1dY_2uLLYu17_3Itf4FWH_I'
                #'key': API_KEY
            }

            # Combine the request url with the parameters above.
            url = combineUrl(STREET_API_URL, params)

            # Retrive image.
            imName = outputDirect + "StreetView-" + str(imageNum).zfill(4) + '.jpg'
            urllib.urlretrieve(url, imName)
            
            # Save data for CSV data set.
            csvDataset.append(imName)
            GPSList[imName] = (gps[0].lat, gps[0].lng)
            
            # Record street view points.
            SVPoint.append((gps[0].lat, gps[0].lng))
            imageNum += 1

        if path.next != None: 
            path = path.next

    # Get the last image.
    # Parameters for API
    params = {
        # Image size; max=600x400
        'size':'600x400', 
        # Horizontal field of view; max=120 
        'fov':'120',  
        # The up or down angle of the camera relative to the Street View vehicle;  
        # 90=sky, -90=floor, 0=front    
        'pitch':'0',       
        # The compass bearing; 0~360; 0=North, 90=East, 180=South, 270=West                   
        'heading':str(bearing), 
        # Current GPS point 
        'location':str(path.lat) + ',' + str(path.lng),
        # Google API key
        'key':'AIzaSyCLP5d5vcwI1dY_2uLLYu17_3Itf4FWH_I'
        #'key': API_KEY
    }

    # Combine the request url with the parameters above.
    url = combineUrl(STREET_API_URL, params)
    
    # Retrive image.
    imName = outputDirect + "StreetView-" + str(imageNum).zfill(4) + '.jpg'
    urllib.urlretrieve(url, imName)
    
    # Save data for CSV data set.
    csvDataset.append(imName)
    GPSList[imName] = (path.lat, path.lng)

    # Record street view point.
    SVPoint.append((path.lat, path.lng))
    #=== Getting last image finished ===


    # Upload images to Google Drive.
    lastForderName = outputDirect.strip().split("/")[-2]
    links = GDriveUpload(csvDataset, FOLDER_NAME + "-" + lastForderName)

    # Prepare dataset for a csv file.
    csvDataset = []
    for link in links:
        csvDataset.append([link.strip().split("/")[-1], links[link], GPSList[link]])
    
    # Sort the GPS data by date and time.
    csvDataset = sorted(csvDataset)
    
    # Insert the titles of the columns.
    csvDataset.insert(0,['Image name', 'Image', 'GPS'])
    
    # Write data to a csv file.
    outputCSV(csvDataset, outputDirect + "GoogleStreetView.csv")

    return SVPoint

