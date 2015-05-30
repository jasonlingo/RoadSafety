"""video file type"""
VideoType = ".MP4"


"""GPS file type"""
GPSType = ".gpx"


"""the length for each shorter video"""
videolenth = 60


"""output image frame quality"""
#in percent
imageQual = 100


"""flip image"""
flipImage = True


"""output image frame size"""
#the length of the longest side of a frame image
#the original length is 1920
resizeX = 1200


"""the GPS distance between every video frame"""
#kilometer
GPSDistance = 0.1


"""timezone for GPS"""
#the GPS recorder is based on UTC/GMT+0 time, so it needs to be calibrated.
GPSTimeZone = -5


"""******************************************"""
#Directories
"""the directory of the videos"""
Vdirectory = "media/"


"""the directory of GPS files"""
Gdirectory = "GPS/"


"""directory for splitted videos"""
VOutDirect = Vdirectory + "out/"


"""directory for video frames"""
VFrameDirect = "VideoFrame/"


