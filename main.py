#!/usr/bin/env python
import sys
import GPXdata
import FileUtil
import VideoUtil
import parameter
from collections import defaultdict



def main():
    """Splitting videos into shorter videos and mapping GPS data to each shorter videos."""
    

    """get the video file name list in a given directory"""
    videos = FileUtil.getFilename(parameter.Vdirectory, parameter.VideoType)


    """load GPX data in a given directory"""
    GPXs = FileUtil.getFilename(parameter.Gdirectory, parameter.GPSType)
    gpsData = []
    for GPX in GPXs:
        gpsData += GPXdata.parseGPX(parameter.Gdirectory + GPX)
    gpsData = sorted(gpsData)


    """split videos into shorted ones"""
    for video in videos:
    	print type(VideoUtil.calculate_time("2015-04-29 07:55:39", 120))
    	break	
    	creation_time = VideoUtil.creation_time(parameter.Vdirectory+video)
    	VideoUtil.VideoSplit(parameter.Vdirectory, video, parameter.videolenth, creation_time, gpsData)
    #print VideoUtil.creation_time(parameter.Vdirectory + "GOPR0012.MP4")
    #print VideoUtil.creation_time("media/out/GOPR0012-0.MP4")
    #print VideoUtil.creation_time("media/out/GOPR0012-9.MP4")
    
    	
    """mapping GPS data into videos"""
    #print GPXdata.mapGPS(gpsData, "2015-04-29 07:55:39")







if __name__ == '__main__':
    main()
