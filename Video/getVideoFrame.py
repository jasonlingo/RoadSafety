import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import cv, cv2
from Util.TimeStringToDatetime import TimeStringToDatetime
from Video.videoCreationTime import videoCreationTime
from Image.FlipResizeImage import FlipResizeImage
from Video.nextFrameNum import nextFrameNum
from GPS.FindPathByDist import FindPathByDist
from GPS.searchGPS import searchGPS
from Google.Drive import GDriveUpload
from Google.showPath import showPath
from File.outputCSV import outputCSV
from config import GOPRO_CALI_TIME, FOLDER_NAME


def getVideoFrame(gpsData, filename, flip, resize, outputDirectory, gpsDistance):
    """
    Get video frames every gpsDistance (kilometer)

    Args:
      (list) gpsData: GPS data list
      (String) filename: the name of the video that is going to be processed
      (boolean) flip: If True, then flip the frame images upside down; 
                      If False, then not flip the frame images
      (int) resize: the maximum width of a image
      (String) outputDirectory: the directory of output data
      (int) gpsDistance: the distance (in km) between every two consecutive extraced images
    """
    # Get video creation time (can only read .MP4 file)
    videoCreateTime = videoCreationTime(filename)
    if videoCreationTime == -1:
        # Get creation time error, end the process
        return None

    # The index of the first data that is nearest to the videoCreateTime
    GPSStartIdx = searchGPS(gpsData, videoCreateTime)
    nextGPSIdx = GPSStartIdx 
    
    # Get video file name. Ex: "media/filename.MP4" => "filename"
    # Use this name as the main filename of extracted images
    name = filename.split('/')[-1].split(".")[0]

    # Open video
    vc = cv2.VideoCapture(filename)
    if vc.isOpened():
        success , frame = vc.read()
    else:
        success = False
    
    # Video frame rate per second
    # The frame rate is about 29.97 FPS(frame per second)
    fps = vc.get(cv.CV_CAP_PROP_FPS)
    
    # Initialize data sets
    # Dataset that is going to be written to a csv file
    csvDataset = []
    # For showing points on a map
    framePoint = [] 
    # A list that assists creating a csv data set
    GPSList = {}
    # The count of extraced images
    imageNum = 1
    # The video frame number
    nextFrame = 1

    while success:
        print "output image number: " + str(imageNum).zfill(4)
        
        # The file name of extracted images
        imName = outputDirectory + name + "-" + str(imageNum).zfill(4) + '.jpg'
        cv2.imwrite(imName,frame)
        csvDataset.append(imName)
        
        # Flip image or resize image if needed
        FlipResizeImage(imName, flip, resize)
        imageNum += 1
        
        # Store points for showing points on a map
        framePoint.append((gpsData[nextGPSIdx][1][0], gpsData[nextGPSIdx][1][1]))
        # Store points for writing to a csv file
        GPSList[imName] = (gpsData[nextGPSIdx][1][0], gpsData[nextGPSIdx][1][1])
        print "GPS: " + str(gpsData[nextGPSIdx][0]) + "-->" + str(gpsData[nextGPSIdx][1])
        
        # Find the next GPS time according to the gpsDistance
        nextGPSIdx, GPSTime = FindPathByDist(gpsData, nextGPSIdx, gpsDistance)
        # Find next output frame number
        nextFrame = nextFrameNum(videoCreateTime, GPSTime, fps)
        # Set video frame to nextFrame 
        vc.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, nextFrame)
        # Read the video frame
        success, frame = vc.read()

    vc.release()

    # Upload photos to Google Drive
    # Get a dictionary of photos and their public url
    links = GDriveUpload(csvDataset, FOLDER_NAME)
    
    # Output data to csv file
    csvDataset = []
    for link in links:
        # Record: [filename, link, GPS data]
        csvDataset.append([link.strip().split("/")[-1], links[link], GPSList[link]])
    # Sort records by filename
    csvDataset = sorted(csvDataset)
    # Insert the titles of columns to the first record
    csvDataset.insert(0,['Image name', 'Image', 'GPS'])
    # Output records to a csv file
    outputCSV(csvDataset, outputDirectory + "mode1.csv")

    # Draw GPS path and frame points on a map
    path = []   
    # extract the GPS point of this video
    for gps in gpsData[GPSStartIdx:nextGPSIdx]: 
        path.append((gps[1][0], gps[1][1])) # latitude, longitude
    # Call the function to show the path on a map
    showPath(path , framePoint, outputDirectory)  

