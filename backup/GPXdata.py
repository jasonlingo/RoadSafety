import gpxpy
import gpxpy.gpx
import datetime
from config import GPS_TIME_ZONE
from math import radians, cos, sin, asin, sqrt


def FindPathDist(gpsData, startIdx, distance):
    """
    Find the path according to a given starting point (index of GPS data set) and distance
    

    """
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
    return original_time + datetime.timedelta(0, 0, 0, 0, 0, GPS_TIME_ZONE+1) #(days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])


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

