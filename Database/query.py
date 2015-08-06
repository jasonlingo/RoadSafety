import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import sqlite3 as lite
from config import DATABASE_ADDRESS

conn = lite.connect('taxi_ems.db')
c = conn.cursor()

command = '''
select * from Experiment;
'''

c.execute(command)

result = c.fetchall()
for r in result:
    print r