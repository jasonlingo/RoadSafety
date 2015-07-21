import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import datetime


def TimeZoneCalibrate(originalTime, timezone):
    """
    Adjust the original time to the current time zone.

    Args:
      (datetime) original_time: the original time in UTC 0.
      (int) timezone: the current time zone with respect to UTC 0.
    Return:
      (datetime) the adjusted time.
    """
    
    # The parameter of timedelta:
    # timedelta(days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
    newTime = originalTime + datetime.timedelta(0, 0, 0, 0, 0, timezone+1) 
    return newTime