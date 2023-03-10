import json
import sqlite3

# Load the teams_status.json file
with open('teams_status.json', 'r') as file:
    data = json.load(file)

# Connect to the SQLite database
conn = sqlite3.connect('test.db')
c = conn.cursor()

# Create a table in the database
c.execute('''CREATE TABLE IF NOT EXISTS teams_status
             (id TEXT PRIMARY KEY,
              password TEXT,
              flags TEXT,
              score INTEGER,
              color TEXT)''')

# Insert the data into the table
for key, value in data.items():
    flags = json.dumps(value['flags'])  # Convert the flags list to a JSON string
    c.execute('''INSERT INTO teams_status
                 (id, password, flags, score, color)
                 VALUES (?, ?, ?, ?, ?)''',
              (key, value['password'], flags, value['score'], value['color']))
# Save changes to the database
conn.commit()
with open('flags.json', 'r') as f:
    data = json.load(f)


# create table
c.execute('''CREATE TABLE IF NOT EXISTS flag_values
             (flag text, score integer)''')

# insert data into table
for flag, score in data.items():
    c.execute("INSERT INTO flag_values VALUES (?, ?)", (flag, score))

conn.commit()
# Close the database connection
conn.close()
