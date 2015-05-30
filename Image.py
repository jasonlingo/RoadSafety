import sys
import cv, cv2
from PIL import Image
from VideoUtil import creation_time, time_str_to_datetime
from parameter import VFrameDirect, imageQual, resizeX, GPSDistance
from GPXdata import FindPathDist, searchGPS


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
    """get video frames"""
    #@parameter {list} gpsData: GPS data list
    #@parameter {string} filename: the name of the video that is going to be processed
    #@parameter {boolean} flip: True -> flip the frame images upside down; False -> not flip the frame images
    #The frame rate is about 29.97 FPS(frame per second)


    #get video creation time (can only read .MP4 file)
    videoCreateTime = creation_time(filename)
    #the index of the first data that is nearest to the videoCreateTime
    GPSStartIdx = searchGPS(gpsData, time_str_to_datetime(videoCreateTime))
    #get video file name "media/filename.MP4" => "filename"
    _, name = filename.split(".")[0].split("/")


    #open video
    vc = cv2.VideoCapture(filename)
    if vc.isOpened():
        rval , frame = vc.read()
    else:
        rval = False
    
    #video frame rate per second
    fps = vc.get(cv.CV_CAP_PROP_FPS)

    imageNum = 1
    frameNum = 1
    nextFrame = 1
    while rval:
        if frameNum == nextFrame:
            print "output: " + str(frameNum)
            """write time to the filename"""
            imName = VFrameDirect + name + "-" + str(imageNum) + '.jpg'
            cv2.imwrite(imName,frame)
            if flip or resize:
                processImage(imName, flip, resize)
            imageNum += 1
            #find the next GPS time according to the GPSDistance
            GPSStartIdx, GPSTime = FindPathDist(gpsData, GPSStartIdx, GPSDistance)
            #find next output frame number
            nextFrame = nextFrameNum(time_str_to_datetime(videoCreateTime), GPSTime, fps)
            print "nextFrame: " + str(nextFrame)
        rval, frame = vc.read()
        frameNum += 1
        if frameNum % 100 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
        #cv2.waitKey(1)
    
    vc.release()

