from os import walk


def getFilename(directory, filetype):
    """Get all the file names in the directory. Return a list of filename."""
    filenameList = []
    for (dirpath, dirnames, filenames) in walk(directory):
        for filename in filenames:
            if filetype in filename:
                filenameList.append(filename)

        break
    return filenameList

