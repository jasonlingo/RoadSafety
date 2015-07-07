import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import datetime

def nextFrameNum(startTime, endTime, fps):
    """
    Calculate the next frame number according to the start and end time"""
    #@parameter {datetime} startTime
    #@parameter {datetime} endTime
    #@parameter {float} fps
    delta = endTime - startTime
    return int(delta.total_seconds() * fps)