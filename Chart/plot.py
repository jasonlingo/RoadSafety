import numpy as np
import matplotlib.pyplot as plt



def lineChart(dataset, xLabel, yLabel, outputDirectory):
    """
    Draw experiment data on a line chart.

    Args:
      (XYNode) dataset: the dataset of this chart.
    """
    # Get the two lists that contains data of x and y respectively.
    XList, YList = dataset.toLists()

    plt.plot(XList, YList, '-')
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.show()
    plt.savefig(outputDirectory)
    plt.close()


class XYNode(object):
    """
    A class for storing the x and y paird data for the chart 
    related function. This class is a linked list type.
    """

    def __init__(self, x, y, next=None):
        """
        Constructor.

        Args:
          (float) x: the data of x axis.
          (float) y: the data of y axis.
          (XYNode) next: the next data node.
        """
        self.x = x
        self.y = y
        self.next = next

    def toLists(self):
        """
        Convert this linked list to two lists. One of the two list 
        contains all data of x, and the other contains all data of y.
        
        Return:
          (list) XList: a list of all data of x.
          (list) YList: a list of all data of y.
        """
        XList = []
        YList = []

        # Start from the this node to the end of this linked list.
        pointer = self
        while pointer != None:
            # Output data to the two lists containing x and y respectively.
            XList.append(pointer.x)
            YList.append(pointer.y)
            pointer = pointer.next

        return XList, YList




head = XYNode(10,40)
pointer = head
pointer.next = XYNode(50,30)
pointer = pointer.next
pointer.next = XYNode(200, 25)
pointer = pointer.next
pointer.next = XYNode(500, 18)

lineChart(head, "# of Taxis", "Time to Hospital", "experiment.png")

