import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
#import webbrowser
#from GoogleAPI import findTimeZone
#from time import sleep
#from PIL import Image
#import datetime, pytz
#from config import TRAFFIC_IMAGE_DIRECTORY, GPS_DISTANCE, FOLDER_NAME, OUTPUT_DIRECTORY
#from GoogleStreetView import combineUrl, getBearing
#from GDrive import GDriveUpload
#from FileUtil import outputCSV

def trafficSnapshot(gpsPoint, numOfShot, interval, size):
    """
    Capture traffic snapshots periodically using Google MAP traffic and store those images

    Args:
      (GPSPoint) gpsPoint: the center of the map from which we capture traffic images
      (int) numOfShot: the total number of images that are going to captured
      (int) interval: the interval (in seconds) between two captured images
      (int) size: the size of the map (from 3(big) to 21(detail))
    """
    #create Google MAP with traffic info request url
    url = "https://www.google.com/maps/@" 
    gps = str(gpsPoint.lat) + ',' + str(gpsPoint.lng)
    size = str(size) + "z"
    traffic_param = "/data=!5m1!1e1"
    #combine request url
    url = url + gps + "," + size + traffic_param

    for i in range(numOfShot):
        webbrowser.open(url)
        #wait for the page opens
        sleep(3) 
        #get the current time of the location
        timezone, current_time = findTimeZone(node)
        imgName = TRAFFIC_IMAGE_DIRECTORY + "traffic-" + current_time + ".png"
        command = "screencapture " + imgName
        #screen shot
        os.system(command)
        im = Image.open(imgName)
        #get captured image size
        width, height = im.size
        #crop the captured area, need to be customized depending on different computer
        im.crop((500, 350, width-300, height-30)).save(imgName)
        print imgName + " captured!"
        #program sleeps for the interval time
        sleep(interval)