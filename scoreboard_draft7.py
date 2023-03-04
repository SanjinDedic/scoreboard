
import json, os
import time

directory = ''


#create teams up to hhh with passwords in the teams_status.json --- no new teams allowed
def sign_up():
    team_name=''
    with open(directory + "teams_status.json", "r",encoding='utf-8') as jsonFile:
         team_status = json.load(jsonFile)
    print('CHOOSE YOUR TEAM FROM THE FOLLOWING:')
    for team in team_status:
        print(team)
    while len(team_name) < 3 or len(team_name) > 20:
        team_name = input('Enter your team name:')
    if team_name not in team_status:
        os.system("clear")
        print("TEAM DOES NOT EXIST TRY AGAIN")
        sign_up()
    else:
        password = ''
        while password != team_status[team_name]['password']:
            password = input('Enter your password:')
        return team_name

def menu(my_team):
    print('')
    print('please select from the following options:')
    print('1. Submit flag')
    print('2. See your competition status')
    print('3. Print rankings')
    print('4. Exit')
    choice = input('Enter your choice:')
    if choice == '1':
        flag_submission(my_team)
    elif choice == '2':
        print_status(my_team)
    elif choice == '3':
        print_rankings(my_team)
    elif choice == 'dns':
        live_scoreboard()
    elif choice == '4':
        exit()
    else:
        os.system('clear')
        menu(my_team)


def flag_submission(my_team):
    #are the variables team_status and flag_new used out of scope of with open=
    os.system('cls' if os.name == 'nt' else 'clear')
    flag = input('Enter the flag:')
    with open(directory + "teams_status.json", "r",encoding='utf-8') as jsonFile:
         team_status = json.load(jsonFile)
    with open(directory + "flags.json", "r",encoding='utf-8') as jsonFile:
         flag_new = json.load(jsonFile)
    
    if flag in flag_new and flag not in team_status[my_team]['flags']:
        team_status[my_team]['flags'].append(flag)
        team_status[my_team]['score'] += flag_new[flag]
        if flag != "VCC{5Y573M5_4R3_4_G0}":
            flag_new[flag] -= 1
        print('flag submitted')
        with open(directory + "teams_status.json", "w",encoding='utf-8') as jsonFile:
            json.dump(team_status, jsonFile)
        with open(directory + "flags.json", "w",encoding='utf-8') as jsonFile:
            json.dump(flag_new, jsonFile) 
        menu(my_team)
    elif flag in flag_new and flag in team_status[my_team]['flags']:
        print('flag already submitted')
        menu(my_team)
    else:
        print('invalid flag')
        menu(my_team)

def print_status(my_team):
    with open(directory + "teams_status.json", "r",encoding='utf-8') as jsonFile:
         team_status = json.load(jsonFile)

    os.system('cls' if os.name == 'nt' else 'clear')
    print('my flags:',team_status[my_team]['flags'] )
    print('my score:', team_status[my_team]['score'])
    menu(my_team)
    
#can you highlight your own team
def print_rankings(my_team):
    with open("teams_status.json", "r",encoding='utf-8') as jsonFile:
        temp = json.load(jsonFile)
        teams_d = temp.copy()
    ordered_teams = []
    for score in range(10000,-10,-1):
        for team in temp:
            if temp[team]['score']>= score:
                ordered_teams.append(team)
                del temp[team]
                break
    print('_'*48)
    for team in ordered_teams:
        filler = (15-len(team))*' '
        score = '| SCORE:' + str(teams_d[team]['score'])
        filler2 = (26-len(team+filler+score))*' ' + ' | '
        flags = 'FLAGS TOTAL: '+ str(len(teams_d[team]['flags']))
        if team == my_team:
            print('\033[1;32;40m' + '| '+ team + filler + score + filler2 + flags+'  |' + '\033[0m')
        else:
            print('| '+ team + filler + score + filler2 + flags+'  |')
    print('|'+ '_'*46 + '|')
    input('press any key to go back to menu')
    os.system('clear')
    menu(my_team)

def live_scoreboard():
    colors={'green':"\033[1;32m",
            'red':"\033[1;31m",
            'yellow':"\033[1;33m",
            'blue':"\033[1;34m",
            'magenta':"\033[1;35m",
            'cyan':"\033[1;36m",
            'white':"\033[1;37m"}
    while True:
        with open("teams_status.json", "r",encoding='utf-8') as jsonFile:
            temp = json.load(jsonFile)
            teams_d = temp.copy()
        ordered_teams = []
        for score in range(10000,-10,-1):
            for team in temp:
                if temp[team]['score']>= score:
                    ordered_teams.append(team)
                    del temp[team]
                    break
        print('_'*48)
        count_teams = 0
        for team in ordered_teams:
            if count_teams < 5:
                filler = (15-len(team))*' '
                score = '| SCORE:' + str(teams_d[team]['score'])
                filler2 = (26-len(team+filler+score))*' ' + ' | '
                flags = 'FLAGS TOTAL: '+ str(len(teams_d[team]['flags']))
                print(colors[teams_d[team]['color']]+'| '+ team + filler + score + filler2 + flags+'  |' + '\033[0m')
                count_teams += 1
        print('|'+ '_'*46 + '|')
        time.sleep(5)
        os.system('clear')

def exit():
    print('exit')

team = sign_up()
menu(team)
