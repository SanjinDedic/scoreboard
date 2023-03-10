import  os, time
from legacy_json.scoring import Scoreboard


scoreboard = Scoreboard()
scoreboard.load_teams("teams_status.json")


while True:
    scoreboard.print_rankings()
    time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')