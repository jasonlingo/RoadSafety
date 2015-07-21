import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from dbfread import DBF

def readDBF(filename):

    for record in DBF(filename):
        print record






readDBF("GPS_data/NASA/IND_rds/IND_roads.dbf")
