import sys
import cv, cv2
from PIL import Image
from VideoUtil import creation_time, time_str_to_datetime
from parameter import VFrameDirect, imageQual, resizeX, GPSDistance, csvFilename
from GPXdata import FindPathDist, searchGPS
from FileUtil import outputCSV
from googleMap import showPath


def processImage(filename, flip, resize):
    """flip an image vertically"""
    im = Image.open(filename)
    #flip image upside down
    if flip:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    #resize image (16:9)
    if resize:
        im = im.resize((resizeX, resizeX*9/16), Image.ANTIALIAS)
    #output file with adjusted image quality (imageQual)
    im.save(filename, 'JPEG', quality=imageQual)
    del im


def nextFrameNum(startTime, endTime, fps):
    """calculate the next frame number according to the start and end time"""
    #@parameter {datetime} startTime
    #@parameter {datetime} endTime
    #@parameter {float} fps
    delta = endTime - startTime
    return int(delta.total_seconds() * fps)


def getVideoFrame(gpsData, filename, flip, resize):
    """get video frames every GPSDistance (in kilometers)"""
    #@parameter {list} gpsData: GPS data list
    #@parameter {string} filename: the name of the video that is going to be processed
    #@parameter {boolean} flip: True -> flip the frame images upside down; False -> not flip the frame images
    #The frame rate is about 29.97 FPS(frame per second)


    #get video creation time (can only read .MP4 file)
    videoCreateTime = creation_time(filename)
    #the index of the first data that is nearest to the videoCreateTime
    GPSStartIdx = searchGPS(gpsData, videoCreateTime)
    nextGPSIdx = GPSStartIdx 
    #get video file name "media/filename.MP4" => "filename"
    _, name = filename.split(".")[0].split("/")


    #open video
    vc = cv2.VideoCapture(filename)
    if vc.isOpened():
        success , frame = vc.read()
    else:
        success = False
    
    #video frame rate per second
    fps = vc.get(cv.CV_CAP_PROP_FPS)
    csvDataset = ["Frame Name"] #dataset that is going to be written to a csv file

    framePoint = [] #for showing points on a map
    imageNum = 1
    nextFrame = 1
    while success:
        """write time to the filename"""
        print "output frame: " + str(nextFrame)
        imName = VFrameDirect + name + "-" + str(imageNum) + '.jpg'
        cv2.imwrite(imName,frame)
        csvDataset.append(imName)
        if flip or resize:
            processImage(imName, flip, resize)
        imageNum += 1
        #store points for showing points on a map
        framePoint.append((gpsData[nextGPSIdx][1][0], gpsData[nextGPSIdx][1][1]))
        #find the next GPS time according to the GPSDistance
        nextGPSIdx, GPSTime = FindPathDist(gpsData, nextGPSIdx, GPSDistance)
        #find next output frame number
        nextFrame = nextFrameNum(videoCreateTime, GPSTime, fps)
        print "GPS: " + str(gpsData[nextGPSIdx][0]) + "-->" + str(gpsData[nextGPSIdx][1])
        vc.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, nextFrame)
        success, frame = vc.read()
        #cv2.waitKey(1)
    
    vc.release()

    #output data to csv file
    outputCSV(csvDataset, csvFilename)

    #draw GPS path and frame points on a map
    path = []   
    for gps in gpsData[GPSStartIdx:nextGPSIdx]:
        path.append((gps[1][0], gps[1][1]))
    showPath(path , framePoint)    



"""
def getIntersectionFrame(gpsData, filename, flip, resize):
    #get intersection image fram from a video
    #@parameter {list} gpsData: GPS data list
    #@parameter {string} filename: the name of the video that is going to be processed
    #@parameter {boolean} flip: True -> flip the frame images upside down; False -> not flip the frame images
    #The frame rate is about 29.97 FPS(frame per second)


    #get video creation time (can only read .MP4 file)
    videoCreateTime = creation_time(filename)
    #the index of the first data that is nearest to the videoCreateTime
    GPSStartIdx = searchGPS(gpsData, videoCreateTime)
    nextGPSIdx = GPSStartIdx
    #store GPS path
    path = []

    #get video file name "media/filename.MP4" => "filename"
    _, name = filename.split(".")[0].split("/")


    #open video
    vc = cv2.VideoCapture(filename)
    if vc.isOpened():
        success , frame = vc.read()
    else:
        success = False
    
    #video frame rate per second
    fps = vc.get(cv.CV_CAP_PROP_FPS)

    framePoint = [] #for showing points on a map
    print gpsData[GPSStartIdx][1][0]
    imageNum = 1
    nextFrame = 1
    while success:
        #write time to the filename
        print "output frame: " + str(nextFrame)
        imName = VFrameDirect + name + "-" + str(imageNum) + '.jpg'
        cv2.imwrite(imName,frame)
        if flip or resize:
            processImage(imName, flip, resize)
        imageNum += 1
        #store points for showing points on a map
        framePoint.append((gpsData[GPSStartIdx][1][0], gpsData[GPSStartIdx][1][1]))
        #find the next GPS time according to the GPSDistance
        GPSStartIdx, GPSTime = FindPathDist(gpsData, GPSStartIdx, GPSDistance)
        #find next output frame number
        nextFrame = nextFrameNum(videoCreateTime, GPSTime, fps)
        print "GPS: " + str(gpsData[GPSStartIdx][0]) + "-->" + str(gpsData[GPSStartIdx][1])
        vc.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, nextFrame)
        success, frame = vc.read()
        #cv2.waitKey(1)
    
    vc.release()   
"""
    

