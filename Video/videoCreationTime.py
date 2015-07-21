import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import subprocess
import datetime
from config import GOPRO_CALI_TIME
from Util.TimeStringToDatetime import TimeStringToDatetime


def videoCreationTime(filename):
    """
    Get the creation time of a video.

    Args:
      (String) filename: the name of a video that we want to 
                         extract its creation time
    Return:
      (datetime) time: the creation time of a given video file
    """
    # Use subprocess to execute the command to get the creation time of a video
    cmnd = ['ffprobe', '-show_format', '-pretty', '-loglevel', 'quiet', filename]
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err =  p.communicate()
      
    if err:
        print "========= Get creation time error! ========"
        print err
        return -1
    else:    
        t = out.splitlines()

        # Extract the creation time.
        time = str(t[14][18:37])

        # The time difference .
        delta = datetime.timedelta(0, GOPRO_CALI_TIME)

        # Convert the time from a stirng to datetime type, 
        # then add the time difference to adjust the time.
        time = TimeStringToDatetime(time) + delta
        return time