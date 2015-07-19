import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import datetime

def TimeZoneCalibrate(original_time, timezone):
    """
    Adjust the new creation time to the current time zone.

    Args:
      (datetime) original_time: the original time in UTC 0.
      (timezone) timezone: the current time zone.
    Return:
      (datetime) the adjusted time
    """
    # timedelta(days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
    newTime = original_time + datetime.timedelta(0, 0, 0, 0, 0, timezone+1) 
    return newTime