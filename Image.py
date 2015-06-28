import sys
import cv, cv2
import webbrowser
from PIL import Image
from VideoUtil import creation_time, time_str_to_datetime
from parameter import VIDEO_FRAME_DIRECTORY, IMAGE_QUALITY, RESIZE_X, GPS_DISTANCE, CSV_FILENAME, FOLDER_NAME, OUTPUT_DIRECTORY
from GPXdata import FindPathDist, searchGPS
from FileUtil import outputCSV
from GoogleMap import showPath
from GDrive import GDriveUpload


def processImage(filename, flip, resize):
    """flip an image vertically"""
    im = Image.open(filename)
    #flip image upside down
    if flip:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    #resize image (16:9)
    if resize:
        im = im.resize((RESIZE_X, RESIZE_X*9/16), Image.ANTIALIAS)
    #output file with adjusted image quality (IMAGE_QUALITY)
    im.save(filename, 'JPEG', quality=IMAGE_QUALITY)
    del im


def nextFrameNum(startTime, endTime, fps):
    """calculate the next frame number according to the start and end time"""
    #@parameter {datetime} startTime
    #@parameter {datetime} endTime
    #@parameter {float} fps
    delta = endTime - startTime
    return int(delta.total_seconds() * fps)


def getVideoFrame(gpsData, filename, flip, resize, outputDirectory):
    """get video frames every GPS_DISTANCE (in kilometers)"""
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
    #csvDataset = ["Frame Name"] #dataset that is going to be written to a csv file
    csvDataset = []

    framePoint = [] #for showing points on a map
    GPSList = {}
    imageNum = 1
    nextFrame = 1
    while success:
        """write time to the filename"""
        print "output image number: " + str(imageNum).zfill(4)
        imName = outputDirectory + name + "-" + str(imageNum).zfill(4) + '.jpg'
        cv2.imwrite(imName,frame)
        csvDataset.append(imName)
        if flip or resize:
            processImage(imName, flip, resize)
        imageNum += 1
        #store points for showing points on a map
        framePoint.append((gpsData[nextGPSIdx][1][0], gpsData[nextGPSIdx][1][1]))
        GPSList[imName] = (gpsData[nextGPSIdx][1][0], gpsData[nextGPSIdx][1][1])
        print "GPS: " + str(gpsData[nextGPSIdx][0]) + "-->" + str(gpsData[nextGPSIdx][1])
        #find the next GPS time according to the GPS_DISTANCE
        nextGPSIdx, GPSTime = FindPathDist(gpsData, nextGPSIdx, GPS_DISTANCE)
        #find next output frame number
        nextFrame = nextFrameNum(videoCreateTime, GPSTime, fps)
        vc.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, nextFrame)
        success, frame = vc.read()
        #cv2.waitKey(1)
    
    vc.release()

    #upload photos to Google Drive
    links = GDriveUpload(csvDataset, FOLDER_NAME)
    
    #output data to csv file
    csvDataset = []
    for link in links:
        csvDataset.append([link.strip().split("/")[2], links[link], GPSList[link]])
        #check image link
        #webbrowser.open_new(linkList[link])
    csvDataset = sorted(csvDataset)
    csvDataset.insert(0,['Image name', 'Image', 'GPS'])
    outputCSV(csvDataset, OUTPUT_DIRECTORY + "mode1.csv")
    


    #draw GPS path and frame points on a map
    path = []   
    for gps in gpsData[GPSStartIdx:nextGPSIdx]:
        path.append((gps[1][0], gps[1][1]))
    showPath(path , framePoint, outputDirectory)    
