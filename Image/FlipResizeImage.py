import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PIL import Image
from Video.videoCreationTime import videoCreationTime
from Util.TimeStringToDatetime import TimeStringToDatetime
from config import RESIZE_X, IMAGE_QUALITY


def FlipResizeImage(filename, flip, resize):
    """flip an image vertically"""
    im = Image.open(filename)
    #flip image upside down
    if flip:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    #resize image (16:9)
    if resize:
        im = im.resize((RESIZE_X, RESIZE_X*9/16), Image.ANTIALIAS)
    #output file with adjusted image quality (IMAGE_QUALITY)
    im.save(filename, 'JPEG', quality=IMAGE_QUALITY)
    del im