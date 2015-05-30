#!/usr/bin/env python
import sys
import datetime
import parameter
from Image import getVideoFrame
from GPXdata import parseGPX
from FileUtil import getFilename


def main():
    """Splitting videos into shorter videos and mapping GPS data to each shorter videos."""
    
    
    """get the video file name list in a given directory"""
    videos = getFilename(parameter.Vdirectory, parameter.VideoType)

    """load GPX data in a given directory"""
    GPXs = getFilename(parameter.Gdirectory, parameter.GPSType)
    gpsData = []
    for GPX in GPXs:
        gpsData += parseGPX(parameter.Gdirectory + GPX)
    gpsData = sorted(gpsData)
    for x in gpsData:
        print x

    """check whether or not resize image"""
    if parameter.resizeX == 1920:
        resize = False
    else:
        resize = True

    """get video frames according to the GPS distance"""
    for video in videos:
        getVideoFrame(gpsData, parameter.Vdirectory + video, parameter.flipImage, resize)
        break



if __name__ == '__main__':
    main()
