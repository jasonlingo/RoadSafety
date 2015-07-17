class GPSPoint:
    """
    A class of GPS point with a linked list data structure
    """
    #GPS position
    #lat = None #latitude
    #lng = None #longitude
    
    #direction data
    #distance = 0 #distance (meters) from this node to the next node
    #duration = 0 #time (seconds) from this node to the next node

    #next node
    #next = None
    

    def __init__(self, latitude, longitude, distance=0, duration=0, next=None):
        """Constructor"""
        # GPS positoin
        self.lat  = latitude
        self.lng  = longitude

        # direction data
        self.distance = distance # distance from this node to the next node
        self.duration = duration # time (seconds) from this node to the next node
        
        # next node
        self.next = next


    def printNode(self):
        """print all nodes' data from current node to the last node"""
        print "lat: %8f  lng: %8f  distance: %5dm  duration: %5dsec" %(self.lat, self.lng, self.distance, self.duration)
        if self.next != None:
            self.next.printNode()

    def nodeNum(self):
        """return the number of node from current node to the last one"""
        if self.next == None:
            return 1
        else:
            return 1 + self.next.nodeNum()

    def toList(self):
        """tranform this linked list to a list and return it"""
        GPSList = []
        pointer = self
        while pointer != None:
            # Append all the latitude and longitude to a GPS list
            GPSList.append((pointer.lat, pointer.lng))
            pointer = pointer.next
        return GPSList

    def getTail(self):
        """Return the last node"""
        pointer = self
        while pointer.next != None:
            pointer = pointer.next
        return pointer

    def getTotalDistance(self):
        """Return the total distance from current node to the last node"""
        totDist = 0
        pointer = self
        while pointer != None:
            totDist += pointer.distance
            pointer = pointer.next
        return totDist

    def getTotalDuration(self):
        """Return the total time from current node to the last node"""
        totTime = 0
        pointer = self
        while pointer != None:
            totTime += pointer.duration
            pointer = pointer.next
        return totTime
