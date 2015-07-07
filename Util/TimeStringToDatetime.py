import datetime

def TimeStringToDatetime(timeStr):
    """convert time string into datetime format"""
    #format of timeStr: [2015-04-29 07:55:39]
    year  = int(timeStr[0:4])
    month = int(timeStr[5:7])
    day   = int(timeStr[8:10])
    hh    = int(timeStr[11:13])
    mm    = int(timeStr[14:16])
    ss    = int(timeStr[17:])
    return datetime.datetime(year,month,day,hh,mm,ss)