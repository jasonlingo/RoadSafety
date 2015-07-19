from GPS.GPSPoint import GPSPoint
from config import API_KEY, OUTPUT_DIRECTORY
import time
import json, requests
import datetime, pytz
from pytz import timezone
from datetime import datetime
from GoogleMap import showGrig, findInnerGrid
from GoogleStreetView import getDirection
from FileUtil import outputCSV
from time import sleep
import sys

def findTimeZone(gpsPoint):
    """
    Find time zone according to GPS data by using Google Time Zone API

    Args:
      (GPSPoint) gpsPoint: the GPS of the time zone
    Return:
      time zone
    """

    TIMEZONE_API_URL = "https://maps.googleapis.com/maps/api/timezone/json?"
    #parameters for API
    params = dict(
        location=str(gpsPoint.lat) + ',' + str(gpsPoint.lng),
        timestamp=str(time.time()),
        key=API_KEY
    )
    #get time zone from Google time zone API
    resp = requests.get(url=TIMEZONE_API_URL, params=params)
    #transform response to json format
    data = json.loads(resp.text)
    #get time zone from dict data
    timezoneName = data['timeZoneId']
    #set the time format
    fmt = '%Y-%m-%d_%H-%M-%S'
    #set the local time zone
    eastern = timezone('US/Eastern')
    #find the current time of the target time zone
    targetTZ = timezone(timezoneName)
    loc_dt = eastern.localize(datetime.now())
    target_dt = loc_dt.astimezone(targetTZ)
    
    return timezoneName, target_dt.strftime(fmt)
    

def sumDirectionTIme(directions):
    """
    sum the traffic time for every Google direction, store the result in a csv file

    Args:
      (list) directions: a list of Google directions
    Return:
      (linked list) GPSPoint: return the direction with longest time
    """

    """for check csv"""
    for direction in directions:
        print "----------------"
        direction.printNode()


    csvDataset = [["Latitude", "Longitude", "Distance", "Duration"]]
    longestTime = 0
    longestDist = 0
    longestTimeIdx = 0
    longestDistIdx = 0
    for i, direction in enumerate(directions):
        title = "Direction-" + str(i+1).zfill(4) 
        csvDataset.append([title])
        totalTime = 0
        totalDist = 0
        while(direction!=None):
            totalTime += direction.duration
            totalDist += direction.distance
            csvDataset.append( [direction.lat, direction.lng, direction.distance, direction.duration] )
            direction = direction.next
        csvDataset.append( ["Total distance:", totalDist, "Total duration:", totalTime] )
        csvDataset.append([])
        if totalTime > longestTime:
            longestTime = totalTime
            longestTimeIdx = i+1
        if totalDist > longestDist:
            longestDist = totalDist
            longestDistIdx = i+1


    csvBottom = "The direction with longest duration is: Direction-" + str(longestTimeIdx)
    csvDataset.append( [csvBottom] )
    csvBottom = "The direction with longest distance is: Direction-" + str(longestDistIdx)
    csvDataset.append( [csvBottom] )

    outputCSV(csvDataset, OUTPUT_DIRECTORY+"direction.csv")

    #return the direction with longest time
    return directions[longestTimeIdx-1]



def calcGridTrafficTime(region):
    """
    Calculate the traffic time of grid point in a given region

    Args:
      (Linked list) region: a linked list of GPS node of a region
    """
    #build a rectangle by find the most top, right, left, and bottom of the GPS nodes.
    pointer = region
    top = region
    bottom = region
    left = region
    right = region
    while (pointer != None):
        if pointer.lat > top.lat:
            top = pointer
        if pointer.lat < bottom.lat:
            bottom = pointer
        if pointer.lng > right.lng:
            right = pointer
        if pointer.lng < left.lng:
            left = pointer
        pointer = pointer.next

    #
    recTopRight = GPSPoint(top.lat, right.lng)
    recTopLeft  = GPSPoint(top.lat, left.lng)
    recBotRight = GPSPoint(bottom.lat, right.lng)
    recBotLeft  = GPSPoint(bottom.lat, left.lng)

    regionList = []
    while(region != None):
        regionList.append((region.lat, region.lng))
        region = region.next

    #find the inner point in the region
    gridPoint = findInnerGrid(regionList, recTopRight, recTopLeft, recBotRight, recBotLeft) 

    #get directions for every two nodes in gridPoint
    #ask before perform getting directions since the total 
    #number of direction might be very large    
    print "Total number of directions: " + str(len(gridPoint)*(len(gridPoint)-1)/2)
    continue_flag = raw_input("Continue? (Y/N):")
    if continue_flag == "n" or continue_flag == "N":
        return;

    directions= []
    for i, source in enumerate(gridPoint):
        sys.stderr.write(".")
        sourceStr = str(source.lat) + "," + str(source.lng)
        for destination in gridPoint[i+1:]:
            destStr = str(destination.lat) + "," + str(destination.lng)
            directions.append(getDirection(sourceStr,destStr))
            sleep(0.6) #2 requests per second for free account

    longestTimeDirection = sumDirectionTIme(directions)

    #show grid of the region and get the returned list of grid points
    showGrig(regionList, recTopRight, recTopLeft, recBotRight, recBotLeft, gridPoint, longestTimeDirection)      
    







