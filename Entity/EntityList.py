

class EntityList:
    """
    A linked list of entities with a sentinel points to the 
    head and tail of the linked list.

    """

    def __init__(self, firstNode=None):
        """
        Constructor

        Args:
          (GPSPoint) firstNode: the first node in this linked list
        """
        self.head = firstNode
        self.tail = firstNode


    def insert(self, node):
        """
        Insert a node to the tail.

        Args:
          (GPSPoint) node: the node to be inserted.
        """
        self.tail.next = node
        self.tail = node

    def deleteTail(self):
        """Delete the last item in this list"""
        pass

    def getTail(self):
        """
        Return the last node in this linked list.
        """
        return self.tail

    
    