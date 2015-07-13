import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import datetime

def nextFrameNum(startTime, endTime, fps):
    """
    Calculate the total frame number between the start and end time.

    Args:
      (datetime) startTime
      (datetime) endTime
      (float) fps: frame per second
    Return:
      (int) totFrameNum: total number of frames between the start and end time
    """
    # Calculate the time difference
    delta = endTime - startTime
    # Calculate the total number of frames by multiply the total seconds with fps
    totFrameNum = int(delta.total_seconds() * fps)
    return totFrameNum