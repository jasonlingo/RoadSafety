import datetime

def addTime(creation_time, add_time):
    """output the new creation fime by adding add_time to creation_time"""
    #creation_time {datetime}
    #add_time {int} in second
    #return {datetime}
    #the unit of add_time is second
    
    creation_time = time_str_to_datetime(creation_time)
    new_time = creation_time + datetime.timedelta(0, add_time)
    return new_time