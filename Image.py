import cv2
from PIL import Image
from VideoUtil import creation_time
from parameter import VFrameDirect


def flipImage(filename):
    """flip an image vertically"""
    im = Image.open(filename)
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im.save(filename)
    del im



def getVideoFrame(filename, flip):
    """get video frames"""
    #@parameter {boolean} flip: True -> flip the frame images; False -> not flip the frame images

    #get video creation time
    videoCreateTime = creation_time(filename) #can only read .MP4 file
    #get video file name "media/filename.MP4" => "filename"
    _, name = filename.split(".")[0].split("/")

    #open video
    vc = cv2.VideoCapture(filename)


    if vc.isOpened():
        rval , frame = vc.read()
    else:
        rval = False

    
    c = 1
    while rval:
    """need to calculate the time period according to the GPS distance"""
    """can we jump to specific frame?"""
        rval, frame = vc.read()
        imName = VFrameDirect + name + "-" + str(c) + '.jpg'
        cv2.imwrite(imName,frame)
        
        if flip:
            flipImage(imName)

        c = c + 1
        cv2.waitKey(1)
        
        if c > 30:
    	    break
    vc.release()




getVideoFrame('media/GP010069.MP4')