#load the flag_values table from test.db into a dictionary
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

flag_values = {}
c.execute("SELECT * FROM flag_values")
rows = c.fetchall()
for row in rows:
    flag_values[row[0]] = row[1]
print('flag_values loaded')
print(flag_values)
