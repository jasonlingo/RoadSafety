class GPSPoint:
    """
    A class of GPS point with a linked list data structure
    """

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

    def getDurationMS(self):
        """
        Return the total time in minutes and seconds from current node to the last node.
        """
        totalSecond = self.getTotalDuration()
        second = totalSecond % 60
        minute = (totalSecond - second) / 60   
        return minute, second     

