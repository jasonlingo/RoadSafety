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
    # The "time" is larger than the last item, which has the largest time, 
    # in the gpsData, so return the last index of gpsData
    if time > gpsData[-1][0]:
        return len(gpsData) -1

    # The "time" is smaller than the first item, which has the smallest time, 
    # in the gpsData, so return the first index of gpsData    
    if time < gpsData[0][0]:
        return 0


    # Initialize the start and end indices of this GPS data set
    start = 0
    end = len(gpsData)

    if end == 0:
        # no data for this function to find
        return None

    # Because the GPS data is recorded every 5 seconds, 
    # set the time difference to 5 seconds. 
    # If the difference between the search and target time
    # is less than the time difference, then we found the 
    # GPS record we want.
    diff = datetime.timedelta(0,5) # 5 seconds
    
    # Using binary search
    mid = (start + end) / 2
    while abs(gpsData[mid][0] - time) > diff:
        if time > gpsData[mid][0]:
            start = mid
        else:
            end = mid
        mid = (start + end) / 2
    
    if mid == len(gpsData) - 1:
        return mid
    else:
        #find the nearest time, check which of gpsData[mid][0] and gpsData[mid+1][0] is nearer to the target time
        if abs(gpsData[mid][0] - time) < abs(gpsData[mid + 1][0] - time):
            return mid
        else:
            return mid + 1
