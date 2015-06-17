import os
import webbrowser
from GoogleAPI import findTimeZone
from time import sleep
from PIL import Image
from GPXdata import GPSPoint
import datetime, pytz
from parameter import TRAFFIC_IMAGE_DIRECTORY



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

    for i in range(1, numOfShot+1):
        webbrowser.open(url)
        #wait for the page opens
        sleep(3) 
        #get the current time of the location
        timezone, current_time = findTimeZone(node)
        filename = TRAFFIC_IMAGE_DIRECTORY + "traffic-" + current_time + ".png"
        command = "screencapture " + filename
        #screen shot
        os.system(command)
        im = Image.open(filename)
        #get captured image size
        width, height = im.size
        #crop the captured area
        im.crop((60, 350, width-130, height-30)).save(filename)
        print filename + " captured!"
        #program sleeps for the interval time
        sleep(interval)


def getStreetViewByUrl(gpsPoint):
    """
    Get 
    """
    pass



"""
import os 
for j in range(1):
  for i in range(1):
    os.system('webkit2png -F -W 1280 -H 800 -D img -o test%(imgnum)05d "http://www.google.com/mars/#lat=%(lat).6f&amp;lon=%(lon).6f&amp;zoom=8&amp;map=visible"'  % {'imgnum': j*180+i, 'lon': 2*i-180, 'lat': j-60} )
"""
node = GPSPoint(13.748446,100.5343197)#Bangkok
trafficSnapshot(node, 100, 1795, 13)


