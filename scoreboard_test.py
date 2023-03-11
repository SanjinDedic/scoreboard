from scoring_db import Scoreboard

scoreboard = Scoreboard('test.db')

scoreboard.load_teams()

for team in scoreboard.teams:
    print(team)

scoreboard.teams[3].score += 2222

scoreboard.update_teams()
#Rankings after update
scoreboard.print_rankings()
