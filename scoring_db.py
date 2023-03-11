import json, os, sqlite3

class Team():
    def __init__(self, name, score, flags):
        self.name = name
        self.score = score
        self.flags = set(flags)
        self.all_flags = dict()

    def __str__(self):
        if len(self.name) < 8:
            answer = "TEAM NAME: "+ self.name + "\t\t  SCORE: " + str(self.score) + "\t  FLAGS: " + str(len(self.flags))
        else:
            answer = "TEAM NAME: "+ self.name + "\t  SCORE: " + str(self.score) + "\t  FLAGS: " + str(len(self.flags))
        return answer
    
    def team_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('1. Submit Flag')
        print('2. View Scoreboard')
        print('3. View Team Status')
        print('4. Exit')
        choice = input('Enter your choice:')
        if choice == '1':
            self.flag_submission()
        elif choice == '2':
            pass
    
    def flag_submission(self):
        # team submits flag via input
        # team score update
        # team flags updated
        # flags.json updated
        # teams_status.json updated

        os.system('cls' if os.name == 'nt' else 'clear') #clear screen
        flag = input("Submit a flag: ")
        self.load_db()
        # Guard Statment
        if flag not in self.all_flags:
            print("INVALID FLAG")
            return False
        
        #check if flag already found
        if flag in self.flags:
            print("FLAG ALREADY FOUND")
            return False 

        #edit data
        self.flags.add(flag)
        self.score += self.all_flags[flag]
        print('FLAG ACCEPTED', 'ADDING', self.all_flags[flag], 'POINTS')
        if flag != "VCC{5Y573M5_4R3_4_G0}":
            self.all_flags[flag] -= 1
        for flag in self.all_flags:
            print(flag, self.all_flags[flag])

        self.update_db()

        return True

    def load_db(self):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()

        c.execute("SELECT * FROM flag_values")
        rows = c.fetchall()
        for row in rows:
            self.all_flags[row[0]] = row[1]


    def update_db(self): 
        #update the test.db with the new score and flags
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        flags = json.dumps(list(self.flags))  # Convert the flags list to a JSON string
        c.execute('''UPDATE teams_status
                    SET flags = ?, score = ?
                    WHERE id = ?''',
                    (flags, self.score, self.name))
        conn.commit()
        #update the test.db flag_values table with new flag values
        for flag, val in self.all_flags.items():
            c.execute("UPDATE flag_values SET score = ? WHERE flag = ?", (val, flag))
        conn.commit()
        conn.close()
        

                    
class Scoreboard():
    def __init__(self,database_file):
        self.teams = []
        self.database_file = database_file

    def load_teams(self):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.database_file)
        c = conn.cursor()

        # Execute the SQL query to retrieve all the id values
        c.execute("SELECT id FROM teams_status;")
        rows = c.fetchall()
        team_names = [row[0] for row in rows]
        print('teams loaded')

        # Execute the SQL query to retrieve the data for team "aaa"
        for team_name in team_names:
            c.execute("SELECT password, flags, score, color FROM teams_status WHERE id = ?;", (team_name,))
            row = c.fetchone()
            if row:
                password, flags_json, score, color = row
                flags = json.loads(flags_json)  # Convert the JSON string to a Python list
                self.teams.append(Team(team_name, score, flags))

        # Close the database connection
        conn.close()

    def update_teams(self):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.database_file)
        c = conn.cursor()

        for team in self.teams:
            c.execute("SELECT score, flags FROM teams_status WHERE id = ?;", (team.name,))
            row = c.fetchone()
            if row:
                score, flags_json = row
                flags = json.loads(flags_json)
                team.score = score
                team.flags = set(flags)

        # Close the database connection
        conn.close()

    def print_rankings(self):
        #this function needs to add colors to the teams which are read from the json file
        #os.system('cls' if os.name == 'nt' else 'clear')
        self.update_teams()
        ordered_teams = sorted(self.teams, key=lambda x: x.score, reverse=True)
        for team in ordered_teams:
            print(team)

class Session():
    def __init__(self):
        self.scoreboard = Scoreboard('test.db')
        self.scoreboard.load_teams()
        self.your_team = self.sign_in()

    def sign_in(self):
        team_name=''
        #fetch all the ids from the database
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("SELECT id FROM teams_status;")
        rows = c.fetchall()
        team_names = [row[0] for row in rows]
        print('CHOOSE YOUR TEAM FROM THE FOLLOWING:')
        for team in team_names:
            print(team)
        while len(team_name) < 3 or len(team_name) > 20:
            team_name = input('Enter your team name:')
        if team_name not in team_names:
            os.system("clear")
            print("TEAM DOES NOT EXIST TRY AGAIN")
            self.sign_in()
        else:
            password = input('Enter your password:')
            c.execute("SELECT password FROM teams_status WHERE id = ?;", (team_name,))
            row = c.fetchone()
            if row:
                password_db = row[0]
                if password != password_db:
                    os.system("clear")
                    print("INCORRECT PASSWORD TRY AGAIN")
                    self.sign_in()

        for team in self.scoreboard.teams:
            if team.name == team_name:
                self.your_team = team
                break
        return self.your_team

    def menu(self):
        print('')
        print('please select from the following options:')
        print('1. Submit flag')
        print('2. Print rankings')
        print('3. Exit')
        choice = input('Enter your choice:')
        if choice == '1':
            self.your_team.flag_submission()
            self.menu()
        elif choice == '2':
            self.scoreboard.print_rankings()
            self.menu()
        elif choice == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            print('THANK YOU FOR PLAYING')
            exit()
        else:
            os.system('clear')
            print('INVALID CHOICE')
            self.menu()


if __name__ == '__main__':
    s = Scoreboard()
    s.load_teams()