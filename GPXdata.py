import gpxpy
import gpxpy.gpx
import datetime
import parameter


def TimeZoneCalibrate(original_time):
    """output the new creation fime by adding add_time to creation_time"""
    #creation_time {datetime}
    #return {datetime}
    z = datetime.timedelta(0, 0, 0, 0, 0, parameter.GPSTimeZone) 
    print z
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
