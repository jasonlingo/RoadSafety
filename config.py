VIDEO_TYPE = ".MP4"
"""Video file type"""

GPS_TYPE = ".gpx"
"""GPS file type"""

VIDEO_LENGTH = 60
"""The length for each shorter video"""

IMAGE_QUALITY = 100
"""Output image frame quality (%)"""

FLIP_IMAGE = True
"""Flip extracted images if the original video is recored upside down"""

CSV_FILENAME = "frame.csv"
"""csv filename"""

RESIZE_X = 1200
"""Output image frame size"""

GOPRO_CALI_TIME = -18
"""GoPro time calibration
There might be a difference between the real and recorded creation time
of a video recorded by GoPro. COPRO_CALI_TIME needed to be test in order 
to find the nearest calibration time.
"""

GPS_DISTANCE = 1.0
"""The GPS distance between every video frame (km)"""

GPS_TIME_ZONE = -5.0
"""Timezone for GPS
The GPS recorder is based on UTC/GMT+0 time, so it needs to be calibrated.
"""

GRID_DISTANCE = 8.0
"""Grid distance (km)"""

TAXI_HOT_SPOT_REGION_DIST = 1.0
"""
The distance from the border of a square region to its center 
that is a taxi's hot spot.
"""

HOT_SPOT_THREADHOLD = 0.0
"""
The probability threadhold for taxi's hot spot region.
If the probability of a randomly generated taxi's location is higher than 
this threadhold, then add this taxi's location into a experiment.
"""

NON_HOT_SPOT_THREADHOLD = 0.98
"""
The probability threadhold for region that is not a taxi's hot spot.
If the probability of a randomly generated taxi's location is higher than 
this threadhold, then add this taxi's location into a experiment.
"""

DATABASE_ADDRESS = "Database/taxi_ems.db"
"""The address of experiment database"""

METER_TYPE = "K"
"""Use kilometer (K) or mile (M) for the haversine function"""

EARTH_RADIUS_MILE = 3959.0
"""The radius of the earth in miles"""

EARTH_RADIUS_KM = 6371.0
"""The radius of the earth in kilometers"""

### Directories ###
OUTPUT_DIRECTORY = "output/"
"""The main output directory"""

VIDEO_DIRECTORY = "media/"
"""The directory of the videos"""

GPS_DIRECTORY = "Data/"
"""The directory of GPS files"""

VIDEO_OUTPUT_DIRECTORY = VIDEO_DIRECTORY + "out/"
"""Directory for splitted videos"""

VIDEO_FRAME_DIRECTORY = OUTPUT_DIRECTORY + "VideoFrame/"
"""Directory for output video frames"""

TRAFFIC_IMAGE_DIRECTORY = OUTPUT_DIRECTORY + "Traffic_image/"
"""Directory for cpatured traffic images"""


### Google APIs ###
CLIENT_ID = '789788175176-rm2oshegfhah677o7ipkr048cccla62s.apps.googleusercontent.com'
"""A client id for Google API"""

CLIENT_SECRET = '8A9OL4byJy_S7IprQBAztbmY'
"""The client secret for Google API"""

FOLDER_NAME = "RoadSafety"
"""The forder name on Google Drive for uploading images"""

API_KEY = "AIzaSyCuOTTRq_mfEyzQCBYXnbD9Jr0XDRYnOAg"
"""The API key for Google API"""



