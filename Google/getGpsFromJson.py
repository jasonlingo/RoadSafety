import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint

def getGpsFromJson(jsonGPS):
    """
    Parse direction data from json response data
    
    Args:
      jsonGPS: json file containing direction received from Google MAP direction API
    Return:
      a linked list of GPSPoint
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