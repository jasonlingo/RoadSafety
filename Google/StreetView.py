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
    1.Get street view from Google Street View Image API 
    (https://developers.google.com/maps/documentation/streetview/?hl=pl&csw=1)
    2.Upload images to Google Drive
    3.Output csv file containing image names, links to image, and GPS data

    Args:
      path (linked list): a linked list of GPS point
      outputDirect (string): image output directory
    Return:
      list of Street view points
    """
    STREET_API_URL = 'https://maps.googleapis.com/maps/api/streetview?'
    #the number of total images
    imageNum = 1
    #convert kilometer to meter
    gps_distance_meter = GPS_DISTANCE*1000
    #street view points
    SVPoint = []
    #for output csv
    csvDataset = []
    GPSList = {}
    #for showing the progress
    loop = 0
    while(path.next != None):               
        if loop%10==0:
            sys.stderr.write(".")
            sys.stderr.flush()
        loop+=1
        

        distance = path.distance
        #calculate how many segments in this path
        cutNum = int(round(distance / gps_distance_meter))

        if cutNum > 1:
            # this sub-path is too long, cut it to several shorter pathes
            gpsList = getIntermediatePoint(path, path.next, cutNum)
        elif cutNum == 0:
            # this sub-path is too short (less than 0.5*gps_distance_meter), find the next point 
            # that will make this sub-path longer
            start = path
            while path.next != None:
                if distance + path.next.distance < 1.2*gps_distance_meter:
                    distance += path.next.distance
                    path = path.next
                else:
                    break
            gpsList = [(start, path)]
        else:
            # this sub-path is larger than 0.5*gps_distance_meter and less than 1.5*gps_distance_meter
            gpsList = [(path, path.next)]

        for gps in gpsList:
            bearing = getBearing(gps[0], gps[1])
            #parameters for API
            params = {
                #image size; max=600x400
                'size':'600x400', 
                #horizontal field of view; max=120 
                'fov':'75',  
                #the up or down angle of the camera relative to the Street View vehicle;  
                #90=sky, -90=floor, 0=front    
                'pitch':'0',       
                #the compass bearing; 0~360; 0=North, 90=East, 180=South, 270=West                   
                'heading':str(bearing), 
                #current GPS point 
                'location':str(gps[0].lat) + ',' + str(gps[0].lng),
                #Google API key
                'key':'AIzaSyCLP5d5vcwI1dY_2uLLYu17_3Itf4FWH_I'
                #'key': API_KEY
            }
            #get request url
            url = combineUrl(STREET_API_URL, params)
            #retrive image
            imName = outputDirect + "StreetView-" + str(imageNum).zfill(4) + '.jpg'
            urllib.urlretrieve(url, imName)
            #for output csv
            csvDataset.append(imName)
            GPSList[imName] = (gps[0].lat, gps[0].lng)
            #record street view point
            SVPoint.append((gps[0].lat, gps[0].lng))
            imageNum += 1
        if path.next != None: 
            path = path.next

    #get last image
    #parameters for API
    params = {
        #image size; max=600x400
        'size':'600x400', 
        #horizontal field of view; max=120 
        'fov':'120',  
        #the up or down angle of the camera relative to the Street View vehicle;  
        #90=sky, -90=floor, 0=front    
        'pitch':'0',       
        #the compass bearing; 0~360; 0=North, 90=East, 180=South, 270=West                   
        'heading':str(bearing), 
         #current GPS point 
        'location':str(path.lat) + ',' + str(path.lng),
         #Google API key
        'key':'AIzaSyCLP5d5vcwI1dY_2uLLYu17_3Itf4FWH_I'
    }
    url = combineUrl(STREET_API_URL, params)
    imName = outputDirect + "StreetView-" + str(imageNum).zfill(4) + '.jpg'
    urllib.urlretrieve(url, imName)
    #for output csv
    csvDataset.append(imName)
    GPSList[imName] = (path.lat, path.lng)
    #record street view point
    SVPoint.append((path.lat, path.lng))
     
    #upload images to Google Drive
    lastForderName = outputDirect.strip().split("/")[-2]
    print lastForderName
    links = GDriveUpload(csvDataset, FOLDER_NAME+"-"+lastForderName)

    #output data to csv file
    csvDataset = []
    for link in links:
        csvDataset.append([link.strip().split("/")[-1], links[link], GPSList[link]])
        #check image link
        #webbrowser.open_new(linkList[link])
    csvDataset = sorted(csvDataset)
    csvDataset.insert(0,['Image name', 'Image', 'GPS'])
    outputCSV(csvDataset, outputDirect + "GoogleStreetView.csv")

    return SVPoint