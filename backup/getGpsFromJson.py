import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint


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
        if jsonGPS['status'] == "ZERO_RESULTS":
            return None
