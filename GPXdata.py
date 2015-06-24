import gpxpy
import gpxpy.gpx
import datetime
import parameter
from math import radians, cos, sin, asin, sqrt



class GPSPoint:
    """
    Class of GPS point, containing the latitude and longitude information of a point
    """
    #GPS data
    lat = None #latitude
    lng = None #longitude
    
    #direction data
    distance = 0 #distance (meters) from this node to the next node
    duration = 0 #time (seconds) from this node to the next node

    #next node
    next = None

    def __init__(self, latitude, longitude, distance=0, duration=0):
        """
        set distance and duration to 0 if we don't get the data for those two variable
        """
        self.lat  = latitude
        self.lng  = longitude
        self.distance = distance
        self.duration = duration

    def printNode(self):
        """print all nodes' data from current node to the last node"""
        print "lat: %8f  lng: %8f  distance: %5dm  duration: %5dsec" %(self.lat, self.lng, self.distance, self.duration)
        if self.next != None:
            self.next.printNode()

    def nodeNum(self):
        """return the number of node from current node to the last one"""
        if self.next == None:
            return 1
        else:
            return 1 + self.next.nodeNum()

    def toList(self):
        """tranform linked list to list and return it"""
        GPSList = []
        point = self
        while(point!=None):
            GPSList.append((point.lat, point.lng))
            point = point.next
        return GPSList

    def getTail(self):
        """return the last node"""
        pointer = self
        while pointer.next != None:
            pointer = pointer.next
        return pointer


def haversine(lat1, lng1, lat2, lng2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)

    Args:

    Return:
      distance between two nodes
    """
    # return {kilometer}
    # convert decimal degrees to radians 
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

    # haversine formula 
    dlng = lng2 - lng1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles, 6371 for kilometers
    return c * r


def FindPathDist(gpsData, startIdx, distance):
    """Find the path according to a given starting point (index of GPS data set) and distance"""
    #@parameter {list} gpsData: GPS data list
    #@parameter {int} startIdx: the starting index for searching the gpsData list
    #@parameter {float} distance: in kilometer
    #@return (index, time)
    pathDist = 0
    preGPS = gpsData[startIdx]
    print preGPS
    index = startIdx
    for gps in gpsData[startIdx+1:]:
        tempDist = haversine(preGPS[1][0], preGPS[1][1], gps[1][0], gps[1][1])
        pathDist += tempDist
        preGPS = gps
        index += 1
        if pathDist >= distance:
            break
    print "Dist: " + str(pathDist)
    return index, gpsData[index][0]


def TimeZoneCalibrate(original_time):
    """output the new creation fime by adding add_time to creation_time"""
    #creation_time {datetime}
    #return {datetime}
    return original_time + datetime.timedelta(0, 0, 0, 0, 0, parameter.GPS_TIME_ZONE+1) #(days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])


def parseGPX(GPXfile):
    """parse gpx file and return a list of GPS data"""
    f = open(GPXfile,'r')
    gpx = gpxpy.parse(f)
    gpsData = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                gpsData.append([TimeZoneCalibrate(point.time), (point.latitude, point.longitude, point.elevation)])
                #print 'Point at ({0},{1}) -> {2}, time={3}'.format(point.latitude, point.longitude, point.elevation, point.time)
    return gpsData


def searchGPS(gpsData, time):
    """find the index of the nearest GPS time"""
    #@parameter {list} gpsData: GPS data list
    #@parameter {datetime} time: the time of the GPS data that we want to find
    #@return {int} return the index of the found GPS data in the list
    start = 0
    end = len(gpsData)

    diff = datetime.timedelta(0,5) # 5 seconds
    mid = (start+end)/2
    while abs(gpsData[mid][0] - time) > diff:
        if time > gpsData[mid][0]:
            start = mid
        else:
            end = mid
        mid = (start+end)/2
    if mid == len(gpsData) - 1:
        return mid
    else:
        #find the nearest time, check which of gpsData[mid][0] and gpsData[mid+1][0] is nearer to the target time
        if abs(gpsData[mid][0] - time) < abs(gpsData[mid+1][0] - time):
            return mid
        else:
            return mid + 1

