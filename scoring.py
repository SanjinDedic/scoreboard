import json


class Team():
    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.flags = []

    def __str__(self):
        answer = "TEAM NAME: "+ self.name + "\t  SCORE: " + str(self.score) 

        return answer


class Scoreboard():
    def __init__(self):
        self.teams = []

    def add_team(self, team):
        self.teams.append(team)

    def print_rankings(self):
        ordered_teams = sorted(self.teams, key=lambda x: x.score, reverse=True)
        for team in ordered_teams:
            print(team)

    def print_status(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                print(team)


team_objects= []

with open("teams_status.json", "r",encoding='utf-8') as jsonFile:
    teams_dict = json.load(jsonFile)

for team in teams_dict:
    team_name = team
    score = teams_dict[team]['score']
    flags = teams_dict[team]['flags']
    team_objects.append(Team(team_name, score))


scoreboard = Scoreboard()
scoreboard.teams = team_objects
scoreboard.print_rankings()