import gpxpy
import gpxpy.gpx
import datetime
import parameter
from math import radians, cos, sin, asin, sqrt


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # return {kilometer}
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles, 6371 for kilometers
    return c * r


def FindPathDist(gpsData, startIdx, distance):
    """Find the path according to a given starting point (index of GPS data set) and distance"""
    # parameter {kilometer} distance
    pathDist = 0
    preGPS = gpsData[startIdx]
    index = startIdx
    for gps in gpsData[startIdx+1:]:
        tempDist = haversine(preGPS[1][0], preGPS[1][1], gps[1][0], gps[1][1])
        pathDist += tempDist
        preGPS = gps
        index += 1
        if pathDist >= distance:
            break
    print pathDist
    print gpsData[index]
    return index, pathDist


def TimeZoneCalibrate(original_time):
    """output the new creation fime by adding add_time to creation_time"""
    #creation_time {datetime}
    #return {datetime}
    return original_time + datetime.timedelta(0, 0, 0, 0, 0, parameter.GPSTimeZone+1) #(days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])


def parseGPX(GPXfile):
    """parse gpx file and return a list of GPS data"""
    f = open(GPXfile,'r')
    gpx = gpxpy.parse(f)
    #print gpx
    gpsData = []

    for track in gpx.tracks:
        #print "------"
        for segment in track.segments:
            for point in segment.points:

                gpsData.append([TimeZoneCalibrate(point.time), (point.latitude, point.longitude, point.elevation)])
                #print point
                #print 'Point at ({0},{1}) -> {2}, time={3}'.format(point.latitude, point.longitude, point.elevation, point.time)
    return gpsData


def searchGPS(gpsData, time):
    """find the index of the nearest GPS time"""
    start = 0
    end = len(gpsData)

    diff = datetime.timedelta(0,5)
    mid = (start+end)/2
    while abs(gpsData[mid][0] - time) > diff:
        if time > gpsData[mid][0]:
            start = mid
        else:
            end = mid
        mid = (start+end)/2
    return mid



def mapGPS(gpsData, start, end):
    """find the nearest gps data according to the search_time"""
    #start_idx = searchGPS(gpsData, start)
    #end_idx = searchGPS(gpsData, end)

    pass
