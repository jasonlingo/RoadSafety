import os, sys

def createDirectory(directory):
    """
    Create a directory if it doesn't exist.

    Args:
      (String) directory: the folder address to be created.
    """
    addr = str(os.path.dirname(os.path.realpath(__file__))) + "/"
    if os.path.exists(directory): 
        if not os.path.isdir(directory):
            # it is not a directory, so create a directory
            os.makedirs(directory)
            directory = addr + directory
            sys.stderr.write("Directory: %s created!" % directory)
    else:
        # the directory doesn't exist, so create a directory
        os.makedirs(directory)
        directory = addr + directory
        sys.stderr.write("Directory: %s created!\n" % directory)
    