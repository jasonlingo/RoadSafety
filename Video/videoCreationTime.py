import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import subprocess
#shlex, re, math 
import datetime
#from optparse import OptionParser
#from config import VIDEO_OUTPUT_DIRECTORY, 
from config import GOPRO_CALI_TIME
#from subprocess import call
#import numpy as np
#import cv2
from Util.TimeStringToDatetime import TimeStringToDatetime

def videoCreationTime(filename):
    """get the creation time of a video"""

    cmnd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', filename]
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print filename
    out, err =  p.communicate()
    
    #print "==========output=========="
    #print out
    
    if err:
        print "========= error ========"
        print err
    t = out.splitlines()
    time = str(t[14][18:37])
    delta = datetime.timedelta(0, GOPRO_CALI_TIME)
    time = TimeStringToDatetime(time) + delta
    return time