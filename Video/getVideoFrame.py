import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import cv, cv2
from Util.TimeStringToDatetime import TimeStringToDatetime
from Video.videoCreationTime import videoCreationTime
from Image.FlipResizeImage import FlipResizeImage
from Video.nextFrameNum import nextFrameNum
from GPS.searchGPS import searchGPSByTime, searchGPSByDistance
from Google.Drive import GDriveUpload
from Google.showPath import showPath
from File.outputCSV import outputCSV
from config import GOPRO_CALI_TIME, FOLDER_NAME, IMAGE_QUALITY



def getVideoFrame(gpsData, VideoFilename, flip, resize, outputDirectory, gpsDistance):
    """
    Get video frames every certain distance (gpsDistance).
    Upload extracted images to Google Drive.
    Output images' link and GPS data to a csv file.

    Args:
      (list) gpsData: GPS data list.
      (String) VideoFilename: the name of the video that is going to be processed.
      (boolean) flip: If True, then flip the frame images upside down; 
                      If False, then not flip the frame images.
      (int) resize: the maximum width of a extracted image.
      (String) outputDirectory: the directory of output data
      (int) gpsDistance: the distance (in km) between every two consecutive extraced images
    """
    
    # Get video's creation time (only tested with .MP4 file)
    videoCreateTime = videoCreationTime(VideoFilename)
    if videoCreationTime == -1:
        # Fail to get the creation time, so end this process.
        return None

    # The index of the first data that is nearest to the videoCreateTime.
    GPSStartIdx = searchGPSByTime(gpsData, videoCreateTime)
    nextGPSIdx = GPSStartIdx 
    
    # Get video file name. Ex: "media/filename.MP4" => "filename".
    # Use this name as the main filename of extracted images.
    # Ex. filename-0001.jpg
    name = VideoFilename.split('/')[-1].split(".")[0]

    # Open video
    vc = cv2.VideoCapture(VideoFilename)
    if vc.isOpened():
        success , frame = vc.read()
    else:
        success = False
    
    # Get Video frame rate per second.
    fps = vc.get(cv.CV_CAP_PROP_FPS)
    
    # Initialize data sets.
    # The Dataset that is going to be written to a csv file.
    csvDataset = []
    
    # A list that assists creating a csv data set.
    GPSList = {}

    # For showing points on a map.
    framePoint = [] 

    # The count of extraced images.
    imageNum = 1
    
    # The initial video frame number.
    nextFrame = 1

    while success: # Read video frame successfully.
        print "output image number: " + str(imageNum).zfill(4)
        
        # The file name of extracted images.
        imName = outputDirectory + name + "-" + str(imageNum).zfill(4) + '.jpg'
        
        # Write the image.
        cv2.imwrite(imName,frame)
        csvDataset.append(imName)
        
        # Flip image or resize image if needed.
        FlipResizeImage(imName, flip, resize, IMAGE_QUALITY)

        # Increase the image count for next image.
        imageNum += 1
        
        # Store extracted points for showing them on a map.
        framePoint.append((gpsData[nextGPSIdx][1][0], gpsData[nextGPSIdx][1][1]))
        
        # Store extracted points for writing them to a csv file.
        GPSList[imName] = (gpsData[nextGPSIdx][1][0], gpsData[nextGPSIdx][1][1])
        print "GPS: " + str(gpsData[nextGPSIdx][0]) + "-->" + str(gpsData[nextGPSIdx][1])
        
        # Find the next GPS time according to the gpsDistance.
        nextGPSIdx, GPSTime = searchGPSByDistance(gpsData, nextGPSIdx, gpsDistance)
        
        # Find next output frame number according to the GPSTime.
        nextFrame = nextFrameNum(videoCreateTime, GPSTime, fps)
        
        # Set video frame to nextFrame. 
        vc.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, nextFrame)
        
        # Read the video frame
        success, frame = vc.read()

    vc.release()

    # Upload extracted images to Google Drive.
    # Get a uploaded images and their public url in dictionary format.
    links = GDriveUpload(csvDataset, FOLDER_NAME)
    
    # Output data to a csv file.
    csvDataset = []
    for link in links:
        # Each record: [image filename, link, GPS data].
        csvDataset.append([link.strip().split("/")[-1], links[link], GPSList[link]])
    
    # Sort records by image filename.
    csvDataset = sorted(csvDataset)
    
    # Insert the titles of columns to the first record.
    csvDataset.insert(0,['Image name', 'Image', 'GPS'])
    
    # Output records to a csv file.
    outputCSV(csvDataset, outputDirectory + "mode1.csv")

    # Draw GPS path and extracted images' points on a map.
    path = []   
    # Extract the GPS point of this video.
    for gps in gpsData[GPSStartIdx:nextGPSIdx]: 
        path.append((gps[1][0], gps[1][1])) # latitude, longitude
   
    # Call the function to show the path and extracted images' points on a map.
    showPath(path , framePoint, outputDirectory)  


