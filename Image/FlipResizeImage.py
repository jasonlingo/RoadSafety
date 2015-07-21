import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PIL import Image


def FlipResizeImage(filename, flip, resize, imgQuality):
    """
    1. Flip an image upside down.
    2. Resize image and adjust its image quality.

    Args:
      (String) filename: the image filename
      (boolean) flip: flip the image if it is True.
      (int) resize: the maximum width of this image.
      (int) imgQuality: the quality of this newly saved image.
    """
    # Open this image.
    im = Image.open(filename)
    
    # Flip this image upside down
    if flip:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Resize image and also adjust the image quality
    (width, height) = im.size
    if width > resize:
        ratio = float(height) / float(width)
        #    im.resize( (new width, new height), Image.ANTIALIAS )
        im = im.resize( (resize, int(resize * ratio)), Image.ANTIALIAS)
    
    # Output file with adjusted image quality (IMAGE_QUALITY)
    im.save(filename, 'JPEG', quality=imgQuality)
    
    del im