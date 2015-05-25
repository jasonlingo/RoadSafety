import gpxpy
import gpxpy.gpx


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
                gpsData.append([point.time, (point.latitude, point.longitude, point.elevation)])
                #print point
                #print 'Point at ({0},{1}) -> {2}, time={3}'.format(point.latitude, point.longitude, point.elevation, point.time)
    return gpsData


def mapGPS(gpsData, search_time):
    pass
