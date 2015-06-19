from GPXdata import GPSPoint
from parameter import GPS_DISTANCE, VIDEO_FRAME_DIRECTORY, FOLDER_NAME, OUTPUT_DIRECTORY, API_KEY
from GoogleMap import showPath
from GDrive import GDriveUpload
from FileUtil import outputCSV
import urllib, urllib2
import json, requests
import webbrowser
import math
import time
import pprint
from kml import KmzParser
import xml
import sys


def getBearing(start, end):
    """
    find the compass bearing from start to end
   
    Args:
      start(GPSPoint): the latitude and longitude of the starting point
      end(GPSPoint): the latitude and longitude of the end point
    Return:
      int - The bearing (0~360)
    """
    radians = math.atan2(end.lng-start.lng, end.lat-start.lat)
    bearing = radians * 180.0 / math.pi
    #print 'bearing:', bearing
    return bearing;


def combineUrl(api, params):
    """
    construct url by concatenate api and params
    
    Args:
      api: the url for API
      params(dict): the parameters for the request
    Return:
      a string of url
    """
    url = api 
    length = len(params)
    for i, param in enumerate(params):
        url += param + "=" + params[param]
        if i < length-1:
            url += "&"
    return url


def getIntermediatePoint(start, end, cutNum):
    """
    Get a list of intermediate points between the start and end points.
    Cut the path into cutNum lines

    Args:
      start (GPSPoint): the start point
      end (GPSPoint)  : the end point
      cutNum (int)    : the number of cuts
    Return:
      a list of GPS points
    """
    latDif = (end.lat - start.lat)/cutNum
    lngDif = (end.lng - start.lng)/cutNum
    gpsList = []
    for i in xrange(cutNum): 
    	startPt = GPSPoint(start.lat+latDif*i, start.lng+lngDif*i)
    	endPt = GPSPoint(start.lat+latDif*(i+1), start.lng+lngDif*(i+1))
    	gpsList.append((startPt, endPt))
    return gpsList


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
    imageNum = 1
    gps_distance_meter = GPS_DISTANCE*1000
    #street view points
    SVPoint = []
    #for output csv
    csvDataset = []
    GPSList = {}
    loop = 0
    while(path.next != None):    	        
        if loop%10==0:
            sys.stderr.write(".")
            sys.stderr.flush()
        loop+=1
        
        distance = path.distance
        cutNum = int(round(distance / gps_distance_meter))

        if cutNum > 1:
            #this sub-path is too long, cut it to several shorter pathes
            gpsList = getIntermediatePoint(path, path.next, cutNum)
        elif cutNum == 0:
            #distance is less than 0.5*gps_distance_meter
            start = path
            while path.next != None:
                if distance + path.next.distance < 1.2*gps_distance_meter:
                    distance += path.next.distance
                    path = path.next
                else:
                    break
            gpsList = [(start, path)]
        else:
            gpsList = [(path, path.next)]

        #for x in gpsList:
        #    print x[0].lat, x[0].lng, x[1].lat, x[1].lng
        #print "distance: ", distance

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
    links = GDriveUpload(csvDataset, FOLDER_NAME)

    #output data to csv file
    csvDataset = []
    for link in links:
        csvDataset.append([link.strip().split("/")[-1], links[link], GPSList[link]])
        #check image link
        #webbrowser.open_new(linkList[link])
    csvDataset = sorted(csvDataset)
    csvDataset.insert(0,['Image name', 'Image', 'GPS'])
    outputCSV(csvDataset, OUTPUT_DIRECTORY + "GoogleStreetView.csv")

    return SVPoint


def LinkedListToList(head):
    """
    tranform linked list data to list

    Args:
      LList (linked list): a linked list of GPS data
    Return:
      a list of GPS data
    """
    path = []
    while head != None:
        path.append((head.lat, head.lng)) 
        head = head.next
    return path



def getJSON_GPS(jsonGPS):
    """
    get direction data from json file
    
    Args:
      jsonGPS: json file containing direction received from Google MAP direction API
    Return:
      a linked list of GPS points
    """
    head = GPSPoint(jsonGPS['routes'][0]['legs'][0]['steps'][0]['start_location']['lat'],
    	            jsonGPS['routes'][0]['legs'][0]['steps'][0]['start_location']['lng'],
    	            jsonGPS['routes'][0]['legs'][0]['steps'][0]['distance']['value'],
    	            jsonGPS['routes'][0]['legs'][0]['steps'][0]['duration']['value']) 
    pointer = head
    for data in jsonGPS['routes'][0]['legs'][0]['steps'][1:]:
        pointer.next = GPSPoint(data['start_location']['lat'], 
        	                    data['start_location']['lng'],
        	                    data['distance']['value'],
        	                    data['duration']['value'])
        pointer = pointer.next
    #add last point
    lastIdx = len(jsonGPS['routes'][0]['legs'][0]['steps']) - 1
    pointer.next = GPSPoint(jsonGPS['routes'][0]['legs'][0]['steps'][lastIdx]['end_location']['lat'],
    	                    jsonGPS['routes'][0]['legs'][0]['steps'][lastIdx]['end_location']['lng'])

    return head


def getDirection(originAdd, destAdd):
    """
    Get direction from the starting address to the destination
    
    Args:
      originAdd: the origin GPS position or address
      destAdd: the destination GPS position or address
    Return:
      a linked list of direction
    """
    #API url
    DIRECTION_API_URL = 'https://maps.googleapis.com/maps/api/directions/json?'
    #parameters for API
    params = dict(
        origin=originAdd,
        destination=destAdd,
        departure_time=str(time.strftime("%H%M%S")), #format: HHMMSS
        key=API_KEY
    )
    #get direction from Google MAP API
    resp = requests.get(url=DIRECTION_API_URL, params=params)
    #transform response to json format
    data = json.loads(resp.text)
    
    #get GPS data from json
    head = getJSON_GPS(data)
    #head.printNode()
    return head


