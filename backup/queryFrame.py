from VideoUtil import creation_time

print creation_time("media/GOPR0074.MP4")


"""
vidcap.set(cv2.cv.CV_CAP_PROP_POS_MSEC,20000)      # just cue to 20 sec. position
success,image = vidcap.read()
sec = 20
mse = 40000
while success:
    cv2.imwrite("mediaframe"+str(sec)+"sec.jpg", image)     # save frame as JPEG file
    vidcap.set(cv2.cv.CV_CAP_PROP_POS_MSEC,mse) 
    success,image = vidcap.read() 
    print success
    print mse
    mse += mse
    sec += sec
"""