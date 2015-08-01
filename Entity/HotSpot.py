from GPS.GPSPoint import GPSPoint


class HotSpot(object):
    """
    A class that store the top, bottom, right, and left border 
    of a given taxi's hot spot region.
    """

    def __init__(self, top, bottom, right, left):
        """
        Constructor.

        Args:
          (float) top, bottom, right, left: the borders of this 
                  rectangle/square region.
        """
        # Keep the border information.
        self.top    = top
        self.bottom = bottom
        self.right  = right
        self.left   = left

    def containPoint(self, lat, lng):
        """
        Check whether the point (lat, lng) is inside this region.

        Args:
          (float) lat, lng: the given point's latitude and longitude.
        Return:
          (boolean) True: if the point is inside this region; 
                    False: otherwise.
        """
        #print "-------------------------------------------"
        #print self.bottom, lat, self.top
        #print self.left, lng, self.right
        #print lat >= self.bottom and lat <= self.top and \
        #       lng >= self.left and lng <= self.right
        return lat >= self.bottom and lat <= self.top and \
               lng >= self.left and lng <= self.right


    class Point(object):
        """
        A class that stores a GPS point's latitude and longitude.
        """

        def __init__(self, lat, lng):
            """Constructor

            Args:
              (float) lat, lng: the latitude and longitude of this point.
            """
            self.lat = lat
            self.lng = lng


