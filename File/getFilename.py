from os import walk

def getFilename(directory, filetype):
    """
    Get all the name of files match the filetype in the directory. 
    
    Args:
      (String) directory: the directory that we want to find 
                          all the file of the desinated filetype.
      (String) filetyp: the file type we want to find. (ex ".MP4")
    Return:
      (list) a list of filename.
    """
    filenameList = []
    for (dirpath, dirnames, filenames) in walk(directory):
        for filename in filenames:
            if filetype in filename: 
                # Only find the files that are in the filetype format
                filenameList.append(filename)
        # Only search the files in the first layer of the given directory
        break

    return filenameList

