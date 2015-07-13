import os

def createDirectory(directory):
    """
    Create a directory if it doesn't exist.

    Args:
      (String) directory: the folder address to be created.
    """
    if os.path.exists(directory): 
        if not os.path.isdir(directory):
            # It is not a directory, so create a directory
            os.makedirs(directory)
    else:
        # The directory doesn't exist, so create a directory
        os.makedirs(directory)
    