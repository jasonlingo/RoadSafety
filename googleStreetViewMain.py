from GPXdata import GPSPoint
from parameter import GPS_DISTANCE, VIDEO_FRAME_DIRECTORY
from googleMap import showPath
import urllib, urllib2
import json, requests
import webbrowser
import math
import time
import pprint
import sys

from kml import KmzParser
import xml


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
    for param in params:
        url += param + "=" + params[param] + "&"
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
    Get street view from Google Street View Image API 
    (https://developers.google.com/maps/documentation/streetview/?hl=pl&csw=1)

    Args:
      path (linked list): a linked list of GPS point
      outputDirect (string): image output directory
    Return:
      list of Street view points
    """
    #example: https://maps.googleapis.com/maps/api/streetview?size=600x400&location=40.720032,-73.988354&fov=90&heading=235&pitch=10
    STREET_API_URL = 'https://maps.googleapis.com/maps/api/streetview?'
    imageNum = 1
    #street view points
    SVPoint = []
    while(path.next != None):    	
        #parameters for API
        if imageNum%10 == 0:
        	sys.stderr.write('.')
        	sys.stdout.flush()
        distance = path.distance
        cutNum = int(round(distance / (GPS_DISTANCE*1000)))
        if cutNum > 1:
        	gpsList = getIntermediatePoint(path, path.next, cutNum)
        else:
        	gpsList = [(path, path.next)]

        for gps in gpsList:
            bearing = getBearing(gps[0], gps[1])
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
                'location':str(gps[0].lat) + ',' + str(gps[0].lng)
            }
            #get request url
            url = combineUrl(STREET_API_URL, params)
            #open image
            #webbrowser.open_new(url)
            #store image
            imName = outputDirect + "StreetView-" + str(imageNum).zfill(3) + '.jpg'
            urllib.urlretrieve(url, imName)
            #record street view point
            SVPoint.append((gps[0].lat, gps[0].lng))
            imageNum += 1
            time.sleep(0.2)
        path = path.next

    #get last image
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
         'location':str(path.lat) + ',' + str(path.lng)
    }
    url = combineUrl(STREET_API_URL, params)
    imName = outputDirect + "StreetView-" + str(imageNum).zfill(3) + '.jpg'
    urllib.urlretrieve(url, imName)
    SVPoint.append((path.lat, path.lng))
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
        departure_time=str(time.strftime("%H%M%S")) #format: HHMMSS
    )
    #get direction from Google MAP API
    resp = requests.get(url=DIRECTION_API_URL, params=params)
    #transform response to json format
    data = json.loads(resp.text)
    #pprint.pprint(data)
    #get GPS data from json
    head = getJSON_GPS(data)
    head.printNode()
    return head


def road():
    """
    Get all gps data along a route

    Args:

    Return:
      a list of GPS points along a given route
    """
    ROAD_API_URL = 'https://roads.googleapis.com/v1/snapToRoads?'
    params = dict(
        #path='39.336881,-76.6244629|39.3330933,-76.6257722|39.3329418,-76.62812939999999|39.3222026,-76.6280012|39.3210507,-76.6268723|39.3183694,-76.6296745|39.3025917,-76.6115682|39.3000233,-76.6116783|39.2965022,-76.6113835|39.2976857,-76.6094936|39.2985045,-76.5908606|39.2979582,-76.590825',
        path='39.336881,-76.6244629|39.2979582,-76.590825',
        interpolate='true',
        key='AIzaSyCLP5d5vcwI1dY_2uLLYu17_3Itf4FWH_I'
    )
    resp = requests.get(url=ROAD_API_URL, params=params)
    data = json.loads(resp.text)
    gpsList = []
    for x in data['snappedPoints']:
        gpsList.append((x['location']['latitude'], x['location']['longitude']))
    return gpsList


def main():
    """
    1. Input addresses for start and end points, 
    2. Get direction from Google MAP API, 
    3. Extrace GPS data from direction,
    4. Get and store street view images according to GPS and bearing,
    5. Show path and street view points on Google map.
    """
    #start = GPSPoint(39.299082523,-76.589570718)
    #end = GPSPoint(39.299560499, -76.590062392)
    #path = [start, end] 

    #get detail GPS point list and linked list
    path, head = KmzParser("direction.kmz")

    #path = road()
    #print len(path)
    #showPath(path, viewpoint)

    """
    #get direction
    head = getDirection('500 West University Parkway, Baltimore', '615 N Wolfe St Baltimore, MD 21205')
    #Google map direction path
    path = LinkedListToList(head)
    #street view points
    SVPoint = getStreetView(head, VIDEO_FRAME_DIRECTORY)
    #show path and street view points on Google Map
    showPath(path, SVPoint)
    """
if __name__ == '__main__':
    main()
