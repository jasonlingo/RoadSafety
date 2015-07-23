import os


def createDirectory(directory):
    """
    Create a directory if it doesn't exist.

    Args:
      (String) directory: the folder's address to be created.
    """
    if not os.path.isdir(directory):
        # It is not an existing directory, so create a directory.
        os.makedirs(directory)
    