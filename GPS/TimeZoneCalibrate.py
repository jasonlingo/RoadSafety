import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import datetime
from config import GPS_TIME_ZONE

def TimeZoneCalibrate(original_time):
    """output the new creation fime by adding add_time to creation_time"""
    #creation_time {datetime}
    #return {datetime}
    return original_time + datetime.timedelta(0, 0, 0, 0, 0, GPS_TIME_ZONE+1) #(days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])