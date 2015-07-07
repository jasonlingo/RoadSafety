import datetime

def searchGPS(gpsData, time):
    """
    Find the index of the nearest GPS according to the given time

    Args:
      (list) gpsData: list of GPS data
      (datetime) time: the time of the GPS data that this function is
                       going to find
    Return:
      (int) return the index of the found GPS data in the list
    """
    start = 0
    end = len(gpsData)

    if end == 0:
        return None

    diff = datetime.timedelta(0,5) # 5 seconds
    #using binary search
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