"""video file type"""
VIDEO_TYPE = ".MP4"

"""GPS file type"""
GPS_TYPE = ".gpx"

"""the length for each shorter video"""
VIDEO_LENGTH = 60

"""output image frame quality"""
#in percent
IMAGE_QUALITY = 100

"""flip image"""
FLIP_IMAGE = True

"""csv filename"""
CSV_FILENAME = "frame.csv"

"""output image frame size"""
#the length of the longest side of a frame image
#the original length is 1920
RESIZE_X = 1200

"""GoPro time calibration"""
#there is a difference between the real time and the recorded time in the video file
#real creation time = recorded time + GOPRO_CALI_TIME
GOPRO_CALI_TIME = -18

"""the GPS distance between every video frame"""
#kilometer
GPS_DISTANCE = 0.2

"""timezone for GPS"""
#the GPS recorder is based on UTC/GMT+0 time, so it needs to be calibrated.
GPS_TIME_ZONE = -5

"""Grid distance"""
#in kilometer
GRID_DISTANCE = 13


"""Directories*******************************"""
OUTPUT_DIRECTORY = "output/"

"""the directory of the videos"""
VIDEO_DIRECTORY = "media/"

"""the directory of GPS files"""
GPS_DIRECTORY = "GPS/"

"""directory for splitted videos"""
VIDEO_OUTPUT_DIRECTORY = VIDEO_DIRECTORY + "out/"

"""directory for output video frames"""
VIDEO_FRAME_DIRECTORY = OUTPUT_DIRECTORY + "VideoFrame/"

"""directory for cpatured traffic images"""
TRAFFIC_IMAGE_DIRECTORY = OUTPUT_DIRECTORY + "Traffic_image/"


"""Google API********************************"""
CLIENT_ID = '789788175176-rm2oshegfhah677o7ipkr048cccla62s.apps.googleusercontent.com'
CLIENT_SECRET = '8A9OL4byJy_S7IprQBAztbmY'
FOLDER_NAME = "RoadSafety"
API_KEY = "AIzaSyBMZezl7cpS3jJN3jlA-dDJxi7WAV1kHgU"
