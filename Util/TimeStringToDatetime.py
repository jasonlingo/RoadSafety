import datetime


def TimeStringToDatetime(timeStr):
    """
    Convert time string into datetime format

    Args:
      (String) timeStr: the string represents a time. 
                        The format of timeStr is [2015-04-29 07:55:39]
    Return:
      (datetime) return the converted time in datetime format.
    """
    
    year  = int(timeStr[0:4])
    month = int(timeStr[5:7])
    day   = int(timeStr[8:10])
    hh    = int(timeStr[11:13])
    mm    = int(timeStr[14:16])
    ss    = int(timeStr[17:])
    return datetime.datetime(year,month,day,hh,mm,ss)