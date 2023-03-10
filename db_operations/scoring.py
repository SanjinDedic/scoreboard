import json, os

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
        self.update_db()

        return True

    def load_db(self):
        '''updates self.all_flags'''
        with open("flags.json", "r",encoding='utf-8') as jsonFile:
            self.all_flags = json.load(jsonFile)


    def update_db(self): 
        '''updates self.all_flags allowing the player to get correct score for submitted flag
        writes the new self.score to the database and updates the value of flags in the database'''
        with open("flags.json", "w",encoding='utf-8') as jsonFile:
            json.dump(self.all_flags, jsonFile, indent=4)
            print('db updated')


        with open("teams_status.json", "r",encoding='utf-8') as jsonFile:
            team_status = json.load(jsonFile)
        team_status[self.name]['score'] = self.score
        team_status[self.name]['flags'] = list(self.flags)
        with open("teams_status.json", "w",encoding='utf-8') as jsonFile:
            json.dump(team_status, jsonFile, indent=4)



class Scoreboard():
    def __init__(self):
        self.teams = []
        self.teams_updated = []

    def load_teams(self, team_data):
        with open(team_data, "r",encoding='utf-8') as jsonFile:
            teams_dict = json.load(jsonFile)

        for team in teams_dict:
            team_name = team
            score = teams_dict[team]['score']
            flags = teams_dict[team]['flags']
            self.teams.append(Team(team_name, score, flags))

    def update_teams(self, team_data):
        self.teams = []
        with open(team_data, "r",encoding='utf-8') as jsonFile:
            teams_dict = json.load(jsonFile)
            jsonFile.close()

        for team in teams_dict:
            team_name = team
            score = teams_dict[team]['score']
            flags = teams_dict[team]['flags']
            self.teams.append(Team(team_name, score, flags))


    def print_rankings(self):
        #this function needs to add colors to the teams which are read from the json file
        os.system('cls' if os.name == 'nt' else 'clear')
        self.update_teams("teams_status.json")
        ordered_teams = sorted(self.teams, key=lambda x: x.score, reverse=True)
        for team in ordered_teams:
            print(team)


class Session():
    def __init__(self):
        self.scoreboard = Scoreboard()
        self.scoreboard.load_teams("teams_status.json")
        self.your_team = self.sign_in()

    def sign_in(self):
        team_name=''
        with open("teams_status.json", "r",encoding='utf-8') as jsonFile:
            team_status = json.load(jsonFile)
        print('CHOOSE YOUR TEAM FROM THE FOLLOWING:')
        for team in team_status:
            print(team)
        while len(team_name) < 3 or len(team_name) > 20:
            team_name = input('Enter your team name:')
        if team_name not in team_status:
            os.system("clear")
            print("TEAM DOES NOT EXIST TRY AGAIN")
            self.sign_in()
        else:
            password = ''
            while password != team_status[team_name]['password']:
                password = input('Enter your password:')
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
