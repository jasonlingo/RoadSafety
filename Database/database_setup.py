#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

"""
This script is used to create a database for storing 
taxis' trajectories and directions from point to point 
in a given region.
"""

exe = raw_input("Are you sure want to continue? [y/n]")

if exe in ["y", "Y"]:
    # Connect DB.
    conn = lite.connect('taxi_ems.db')
    c = conn.cursor()

    # Drop old table before creating tables.
    c.execute('drop table if exists CrashCase;')
    c.execute('drop table if exists Experiment;')
    conn.commit()


    # Create a CrashCase table.
    command = '''
    CREATE TABLE CrashCase (
        id integer,
        experiment_id integer,
        latitude float,
        longitude float,
        crash_happen_date date,
        crash_happen_time time,
        taxi_arrival_time integer,
        time_to_hospital integer
    );
    '''
    c.execute(command)


    # Create a Experiment table.
    command = '''
    CREATE TABLE Experiment (
        id integer primary key,
        num_of_taxi integer,
        num_of_hospital integer,
        num_of_crash integer,
        avg_taxi_arrival_time integer,
        avg_to_hospital_time integer,
        avg_tot_transfer_time integer
    );
    '''
    c.execute(command)

    # Commit changes.
    conn.commit()

    # Close DB
    conn.close()

