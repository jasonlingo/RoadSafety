from zipfile import ZipFile
from GPS.GPSPoint import GPSPoint
from GPS.Haversine import Haversine


def KmzParser(filename):
    """
    Parse kmz file produced by "Google My MAP" service. 
    Extract GPS data to a list.

    Args:
      (String) filename: the name of a kmz file.
    Return:
      (GPSPoint) head: a linked list of GPS points.
    """

    # Open kmz file.
    kmz = ZipFile(filename, 'r')
    # Open the kml file in a kmz file.
    kml = kmz.open('doc.kml','r')

    # Extract coordinates from the kmz file.
    coordinates = []
    for i, x in enumerate(kml):
        if "<coordinates>" in x:
            # The desired data will be the first data with "<coordinates>" keyword.
            coordinates.append(x.replace("<coordinates>","").replace("</coordinates>","").replace("\t","").replace("\n",""))
        if "</LineString>" in x:
            # In a route stored in a kmz file, we only need the first coordinates data.
            # The other two are source and destination points.
            break

    # The flag used for the first point.
    first = True
    
    # The head of GPSPoint linked list.
    head = None 
    
    # The node used to operate the linked list.
    pointer = None
    
    # Extract GPS data.
    for coordinate in coordinates:
        GPSs = coordinate.split()
        for GPS in GPSs:
            lng, lat, _ = GPS.split(",")
            lat = float(lat)
            lng = float(lng)
            if first:
                # Deal with the first point, keep the head of this linked list.
                head = GPSPoint(lat, lng)
                pointer = head
                first = False
            else:
                # Add a new GPSPoint to the tail of this extracted GPS linked list.
                pointer.next = GPSPoint(lat, lng)

                # Calculate the distance between this and next GPS points.
                pointer.distance = Haversine(pointer.lat, pointer.lng,
                                             lat, lng) * 1000
                pointer = pointer.next

    return head

