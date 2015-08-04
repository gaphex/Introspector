__author__ = 'Denis'

import sqlite3
import pandas as pd

conn = sqlite3.connect('database/dumps.db')
df = pd.read_sql('select * from traceroute', conn)
print df