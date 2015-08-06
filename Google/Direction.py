import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from config import API_KEY
from time import sleep, mktime
from datetime import datetime, timedelta
import json, requests
import time


def getDirection(originAdd, destAdd, waypoints=None, departure_time=None):
    """
    Get direction from the starting address to the destination
    
    Args:
      (String) originAdd: the origin GPS position or address
      (String) destAdd: the destination GPS position or address
      (GPSPoint) waypoints: the middle points between source and
                            destination points.
      (datetime) departure_time: the dpearture time of this direction.
    Return:
      (GPSPoint) a linked list of direction
    """
    
    # API url.
    DIRECTION_API_URL = 'https://maps.googleapis.com/maps/api/directions/json?'
    
    # Process departure_time.
    # If using a specific departure time, convert it to seconds from 1/1/1970 midnight 
    # to the specific time.
    if departure_time == None:
        # Using the current time as the departure time.
        currentTime = datetime.now() + timedelta(0, 5)
        dTime = int(time.mktime(currentTime.timetuple()))
    else:
        # Using the specific departure time. 
        # The time must be in the future or current time.
        dTime = int(mktime(departure_time.timetuple()))

    # Parameters for API.
    params = dict(
        # Address or GPS of the source point.
        origin = originAdd,
        # Address or GPS of the destination point.
        destination = destAdd,
        # Intermediate points between source and destination.
        waypoints = waypointsConvert(waypoints), 
        # Return distance in meter.
        unit = 'metric', 
        # Departure time.
        departure_time = dTime,
        # Google API key.
        key = API_KEY
    )

    # Get direction from Google MAP API.
    resp = requests.get(url=DIRECTION_API_URL, params=params)
    
    # Transform response to json format.
    data = json.loads(resp.text)
    
    # Get GPS data from json.
    head = getGpsFromJson(data)

    # For the request limit by Google Direction API.
    # For Free account, the limit is 10 request per second.
    sleep(0.1)

    return head


def waypointsConvert(ways):
    """
    Convert waypoints from GPSPoint linkedlist to a string by 
    concatenating every consecutive points with a '|'  between them.

    Args:
      (GPSPoint) ways: the points of intermediate points between 
                       source and destination points.
    Return:
      (String) the concatenated waypoints string.
    """

    # Initialize waypoints list.
    waypointList = []

    # Append every waypoint into the list.
    while ways != None:
        waypointList.append(str(ways.lat) + "," + str(ways.lng))
        ways = ways.next

    # Concatenating waypoints with a "|" between them.
    waypoints = "|".join(waypointList)

    return waypoints


def getGpsFromJson(jsonGPS):
    """
    Parse Google direction data in json format.
    
    Args:
      (dictionary) jsonGPS: a json file containing direction replied
                            from Google MAP direction API.
    Return:
      (GPSPoint) a linked list of GPSPoint.
    """
    
    # The flag for the first point.
    first = True

    # Add GPS points of the direction.
    # Every route has several legs; every leg has several steps.
    try:
        for leg in jsonGPS['routes'][0]['legs']:
            for data in leg['steps']:
                if first: 
                    # Keep the first point as the head of the linked list.
                    head = GPSPoint(data['start_location']['lat'], 
                                    data['start_location']['lng'],
                                    data['distance']['value'],
                                    data['duration']['value'])
                    first = False
                    pointer = head
                else:
                    pointer.next = GPSPoint(data['start_location']['lat'], 
                                            data['start_location']['lng'],
                                            data['distance']['value'],
                                            data['duration']['value'])
                    pointer = pointer.next
        return head
    except:
        print "An error happened while parsing json data!!"
        print jsonGPS
        return None

