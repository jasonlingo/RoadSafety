import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from GPS.GPSPoint import GPSPoint
from File.Directory import createDirectory
import webbrowser
from Google.findTimeZone import findTimeZone
from time import sleep
from PIL import Image
import datetime, pytz
from config import TRAFFIC_IMAGE_DIRECTORY


def trafficSnapshot(gpsPoint, numOfShot, interval, size):
    """
    Capture traffic snapshots periodically using Google MAP traffic and store those images

    Args:
      (GPSPoint) gpsPoint: the center of the map from which we capture traffic images
      (int) numOfShot: the total number of images that are going to captured
      (int) interval: the interval (in seconds) between two captured images
      (int) size: the size of the map (from 3(big) to 21(detail))
    """
    
    # Create Google MAP with traffic info request url
    url = "https://www.google.com/maps/@" 
    gps = str(gpsPoint.lat) + ',' + str(gpsPoint.lng)
    # The scale of the map.
    size = str(size) + "z"
    # Street view parameter.
    traffic_param = "/data=!5m1!1e1"
    
    # Combine request url
    url = url + gps + "," + size + traffic_param

    # Create the output directory if it doesn't exist.
    createDirectory(TRAFFIC_IMAGE_DIRECTORY)

    for i in range(numOfShot):
        # Open the Google MAP street view on a web browser.
        webbrowser.open(url)
        
        # Wait for the page opens
        sleep(5) 
        
        # Get the current time of the location
        timezone, current_time = findTimeZone(gpsPoint)
        imgName = TRAFFIC_IMAGE_DIRECTORY + "traffic-" + current_time + ".png"
        command = "screencapture " + imgName
        
        # Screen shot
        os.system(command)
        im = Image.open(imgName)
        
        # Get captured image size
        width, height = im.size
        
        # Crop the captured area, need to be customized depending on different computer
        im.crop((500, 350, width-300, height-30)).save(imgName)
        print imgName + " captured!"
        
        # Program sleeps for the interval time
        sleep(interval)


