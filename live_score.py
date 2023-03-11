import  os, time
from scoring_db import Scoreboard


scoreboard = Scoreboard('test.db')
scoreboard.load_teams()


while True:
    scoreboard.print_rankings()
    time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')