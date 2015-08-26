#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: Jason, Li-Yi Lin
"""
import sqlite3 as lite
from zipfile import ZipFile


def ParseHospital(filename):
    """
    Parse hospitals' information from a kmz file produced 
    by "Google My MAP" service. Extract hospitals' name and 
    GPS location.

    Args:
      (String) filename: the file name of a kmz file.
    Return:
      (dictionary) hospitals: a linked list of GPS points.
    """

    # Open kmz file.
    kmz = ZipFile(filename, 'r')
    # Open the kml file in a kmz file.
    kml = kmz.open('doc.kml','r')


    # Extract names and coordinates from the kmz file.
    hospitals = {}
    name = None
    coordinates = None
    start = False # True: start to record the information of hospitals.
    for i, x in enumerate(kml):
        if "<Placemark>" in x:
            start = True
        if start:
            if "<name>" in x:
                name = x.replace("<name>", "").replace("</name>", "").replace("\t","").replace("\n","")
            if "<coordinates>" in x:
                [lng, lat, _] = x.replace("<coordinates>","").replace("</coordinates>","").replace("\t","").replace("\n","").split(",")
                coordinates = (lat, lng)
            if "</Placemark>" in x:
                hospitals[name] = coordinates
                start = False

    return hospitals



def StoreHospitalInfo(filename):
    """
    Extract hospitals' information and then store it in a database.

    Args:
       (String) filename: the file name of a kmz file that stores 
                          the information of hospitals.
    """
    


# Start the process.
StoreHospitalInfo("Data/Hospital.kmz")

