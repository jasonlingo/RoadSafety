#!/usr/bin/env python
import sys
import datetime
import parameter
from Image import getVideoFrame
from GPXdata import parseGPX
from FileUtil import getFilename

import pygmaps 
import webbrowser


def main():
    """Splitting videos into shorter videos and mapping GPS data to each shorter videos."""
    
    
    """get the video file name list in a given directory"""
    videos = getFilename(parameter.VIDEO_DIRECTORY, parameter.VIDEO_TYPE)

    """load GPX data in a given directory"""
    GPXs = getFilename(parameter.GPS_DIRECTORY, parameter.GPS_TYPE)
    gpsData = []
    for GPX in GPXs:
        gpsData += parseGPX(parameter.GPS_DIRECTORY + GPX)
    gpsData = sorted(gpsData)

    #for gps in gpsData:
    #    print gps


    """check whether or not resize image"""
    if parameter.RESIZE_X == 1920:
        resize = False
    else:
        resize = True

    """get video frames according to the GPS distance"""
    for video in videos:
        getVideoFrame(gpsData, parameter.VIDEO_DIRECTORY + video, parameter.FLIP_IMAGE, resize)
        break

    for video in videos:
        #getIntersectionFrame()
        break


if __name__ == '__main__':
    main()
