from cv import *
from FileUtil import getFilename


def detectPeople():
    fileList = getFilename("output/VideoFrame/mode4", ".jpg")
    storage = CreateMemStorage(0)
    for file in fileList:
        img = LoadImage("output/VideoFrame/mode4/" + file)  # or read from camera

        found = list(HOGDetectMultiScale(img, storage, win_stride=(8,8),
                padding=(32,32), scale=1.05, group_threshold=2))



import numpy as np
import cv2

help_message = '''
USAGE: peopledetect.py <image_names> ...

Press any key to continue, ESC to stop.
'''

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


def detectPeople():
    import sys
    from glob import glob
    import itertools as it
    print help_message

    fileList = getFilename("output/VideoFrame/mode4", ".jpg")

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

    for fn in fileList:
        print fn, ' - ',
        try:
            img = cv2.imread("output/VideoFrame/mode4/" + fn)
        except:
            print 'loading error'
            continue

        found, w = hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)
        found_filtered = []
        for ri, r in enumerate(found):
            for qi, q in enumerate(found):
                if ri != qi and inside(r, q):
                    break
            else:
                found_filtered.append(r)
        draw_detections(img, found)
        draw_detections(img, found_filtered, 3)
        print '%d (%d) found' % (len(found_filtered), len(found))
        cv2.imshow('img', img)
        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break
    cv2.destroyAllWindows()


def detectPeople2():
    self.capture = cv.CaptureFromFile(fpath)
    cv.NamedWindow(“Target”, 1)

    # Smooth to get rid of false positives
    cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0)
    
    # Convert the image to grayscale.
    cv.CvtColor(color_image, grey_image, cv.CV_RGB2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
    cv.EqualizeHist(small_img, small_img)

    cascade = cv.Load(“data/HS.xml”)
    faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
    haar_scale, min_neighbors, cv.CV_HAAR_DO_CANNY_PRUNING, min_size)

detectPeople()