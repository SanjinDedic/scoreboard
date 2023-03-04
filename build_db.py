import sqlite3,json

conn = sqlite3.connect('test.db')

c = conn.cursor()

try:
    c.execute('''CREATE TABLE teams (
        team_name text, 
        score integer, 
        flags text)''')
except:
    pass


with open("teams_status.json", "r",encoding='utf-8') as jsonFile:
    teams_dict = json.load(jsonFile)

for team in teams_dict:
    team_name = team
    score = teams_dict[team]['score']
    flags = teams_dict[team]['flags']
    flags = ','.join(flags)
    print(flags)
    c.execute("INSERT INTO teams VALUES (?,?,?)", (team_name, score, flags))

conn.commit()
conn.close()
