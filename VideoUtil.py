#!/usr/bin/env python
import os, sys, subprocess, shlex, re, math, datetime
from optparse import OptionParser
from parameter import VOutDirect
from subprocess import call
from GPXdata import mapGPS


def creation_time(filename):
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
    return time

def time_str_to_datetime(timeStr):
    year  = int(timeStr[0:4])
    month = int(timeStr[5:7])
    day   = int(timeStr[8:10])
    hh    = int(timeStr[11:13])
    mm    = int(timeStr[14:16])
    ss    = int(timeStr[17:])
    return datetime.datetime(year,month,day,hh,mm,ss)


def calculate_time(creation_time, add_time):
    """output the new creation fime by adding add_time to creation_time"""
    #format of creation_time: [2015-04-29 07:55:39]
    #the unit of add_time is second
    original_time = time_str_to_datetime(creation_time)
    new_time = original_time + datetime.timedelta(0,add_time)
    return new_time


def VideoSplit(directory, filename, split_length, creation_time, gpsData):
    """split video into shorter videos with length of split_size"""
    #modified from https://github.com/c0decracker/video-splitter

    length_regexp = 'Duration: (\d{2}):(\d{2}):(\d{2})\.\d+,'
    re_length = re.compile(length_regexp)


    if split_length <= 0:
        print "Split length can't be 0"
        raise SystemExit

    output = subprocess.Popen("ffmpeg -i '"+directory+filename+"' 2>&1 | grep 'Duration'", 
                            shell = True,
                            stdout = subprocess.PIPE
                            ).stdout.read()
    print output
    matches = re_length.search(output)
    if matches:
        video_length = int(matches.group(1)) * 3600 + \
                        int(matches.group(2)) * 60 + \
                        int(matches.group(3))
        print "Video length in seconds: "+str(video_length)
    else:
        print "Can't determine video length."
        raise SystemExit

    split_count = int(math.ceil(video_length/float(split_length)))
    if(split_count == 1):
        print "Video length is less then the target split length."
        raise SystemExit

    
    for n in range(0, split_count):
        new_creation_time = calculate_time(creation_time, split_length*n)
        (latitude, longitude, elevation) = mapGPS(gpsData, new_creation_time)

        split_cmd = "ffmpeg -i '"+directory+filename+"'" + ' -metadata creation_time="' + str(new_creation_time) + '"' + " -vcodec copy "
        
        split_str = ""
        if n == 0:
            split_start = 0
        else:
            split_start = split_length * n
        
        split_str += " -ss "+str(split_start)+" -t "+str(split_length) + \
                    " '"+VOutDirect + filename[:-4] + "-" + str(n) + "." + filename[-3:] + \
                    "'"
        print "About to run: "+split_cmd+split_str
        output = subprocess.Popen(split_cmd+split_str, shell = True, stdout =
                               subprocess.PIPE).stdout.read()

