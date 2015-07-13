from zipfile import ZipFile
from GPS.GPSPoint import GPSPoint
from GPS.Haversine import Haversine


def KmzParser(filename):
    """
    Parse KMZ file produced by Google MAP, extract GPS data to a list

    Args:
      (string) filename: the KMZ file
    Return:
      (GPSPoint) head: a linked list of GPS points
    """
    kmz = ZipFile(filename, 'r')
    kml = kmz.open('doc.kml','r')
    coordinates = []
    for i, x in enumerate(kml):
        if "<coordinates>" in x:
            coordinates.append(x.replace("<coordinates>","").replace("</coordinates>","").replace("\t","").replace("\n",""))
            #the desired data will be the first data with "<coordinates>" keyword
        if "</LineString>" in x:
            #in a route KMZ file, we only need the first coordinates data
            #the other two are source and destination points
            break

    first = True
    head = None #the head of GPSPoint linked list
    pointer = None
    GPSList = []
    for coordinate in coordinates:
        GPSs = coordinate.split()
        for GPS in GPSs:
            lng, lat, _ = GPS.split(",")
            lat = float(lat)
            lng = float(lng)
            if first:
                head = GPSPoint(lat, lng)
                pointer = head
                first = False
            else:
                pointer.next = GPSPoint(lat, lng)
                pointer.distance = Haversine(pointer.lat, pointer.lng,
                                             lat, lng)*1000
                pointer = pointer.next

    return head

