import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PIL import Image
from config import IMAGE_QUALITY


def FlipResizeImage(filename, flip, resize):
    """
    1. Flip an image upside down
    2. Resize image and adjust its image qualityit

    Args:
      (String) filename: the image filename
      (boolean) flip: flip the image if it is True.
      (int) resize: the maximum width of this image.
    """
    # Open this image
    im = Image.open(filename)
    
    # Flip this image upside down
    if flip:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    
    # Resize image (16:9) and also adjust the image quality
    (width, height) = im.size
    if width > resize:
        im = im.resize((resize, resize*9/16), Image.ANTIALIAS)
    
    # Output file with adjusted image quality (IMAGE_QUALITY)
    im.save(filename, 'JPEG', quality=IMAGE_QUALITY)
    
    del im