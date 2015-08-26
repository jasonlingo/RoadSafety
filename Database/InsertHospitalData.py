#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: Jason, Li-Yi Lin
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

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
                coordinates = (float(lat), float(lng))
            if "</Placemark>" in x:
                hospitals[name] = coordinates
                start = False

    return hospitals



def InsertHospitalData(filename, DB):
    """
    Extract hospitals' information and then store it in a database.

    Args:
       (String) filename: the file name of a kmz file that stores 
                          the information of hospitals.
       (String) DB: the file name of the target database.
    """
    # Connect DB.
    conn = lite.connect(DB)
    c = conn.cursor()

    # Delete all the old data.
    c.execute('delete from Hospital')

    # Parse kmz file and get hospitals' information.
    hospitals = ParseHospital(filename)

    # Insert data into database.
    i = 1 # The counter for hospital id.
    for hos in hospitals:
        (lat, lng) = hospitals[hos]
        command = '''
        insert into Hospital values(%d, "%s", %f, %f)
        ''' % (i, hos, lat, lng)
        print command
        c.execute(command)
        i += 1

    conn.commit()
    conn.close()

# Start the process.
InsertHospitalData("Data/Hospital.kmz", "Database/taxi_ems.db")

