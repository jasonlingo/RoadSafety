from os import walk


def getFilename(directory):
    """Get all the file names in the directory. Return a filename list."""
    f = []
    for (dirpath, dirnames, filenames) in walk(directory):
       f.extend(filenames)
       break
    return f