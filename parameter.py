"""video file type"""
VideoType = ".MP4"

"""GPS file type"""
GPSType = ".gpx"

"""the length for each shorter video"""
videolenth = 240

"""the directory of the videos"""
Vdirectory = "media/"

"""the directory of GPS files"""
Gdirectory = "GPS/"

"""directory for splitted videos"""
VOutDirect = Vdirectory + "out/"

"""directory for video frames"""
VFrameDirect = "VideoFrame/"

"""timezone for GPS"""
#the GPS recorder is based on UTC/GMT+0 time, so it needs to be calibrated.
GPSTimeZone = -5
