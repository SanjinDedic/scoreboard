import json
import sqlite3

# Load the teams_status.json file
with open('teams_status.json', 'r') as file:
    data = json.load(file)

# Connect to the SQLite database
conn = sqlite3.connect('test.db')
c = conn.cursor()


with open('reset_flags.json', 'r') as f:
    flag_data = json.load(f)

#update the test.db flag_values table with new flag values
for flag, score in flag_data.items():
    c.execute("UPDATE flag_values SET score = ? WHERE flag = ?", (score, flag))
    print('flag updated', flag, score)
conn.commit()


#open the new flags.json file
with open('new_teams.json', 'r') as f:
    teams_status = json.load(f)

#update the test.db teams_status table with values for each team
for team, team_data in teams_status.items():
    print(team_data['flags'])
    flags = json.dumps(team_data['flags'])  # Convert the flags list to a JSON string
    c.execute('''UPDATE teams_status
                SET flags = ?, score = ?
                WHERE id = ?''',
                (flags, team_data['score'], team))
    print('team updated', team, team_data['score'], flags)

conn.commit()
# Close the database connection
conn.close()
