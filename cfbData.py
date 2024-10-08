import requests
import csv

# *~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~*
# *~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~*

# Predictor for Conference Winner
# which data to pull from
# use record to be able to predict Match ups
ACC = ['Boston College', 'California', 'Clemson', 'Duke', 'Florida State', 'Georgia Tech', 'Louisville', 'Miami', 
       'NC State', 'North Carolina', 'Pittsburgh', 'SMU', 'Stanford', 'Syracuse', 'Virginia', 'Virginia Tech', 'Wake Forest']

B12 = ['Arizona', 'Arizona State', 'Baylor', 'BYU', 'Cincinnati', 'Colorado', 'Houston', 'Iowa State', 
       'Kansas', 'Kansas State', 'Oklahoma State', 'TCU', 'Texas Tech', 'UCF', 'Utah', 'West Virginia']

SEC = ['Alabama', 'Arkansas', 'Auburn', 'Florida', 'Georgia', 'Kentucky', 'LSU', 'Mississippi State', 
       'Missouri', 'Oklahoma', 'Ole Miss', 'South Carolina', 'Tennessee', 'Texas', 'Texas A&M', 'Vanderbilt']

B1G = ['Illinois', 'Indiana', 'Iowa', 'Maryland', 'Michigan', 'Michigan State', 'Minnesota', 'Nebraska', 'Northwestern', 'Ohio State',
       'Oregon', 'Penn State', 'Purdue', 'Rutgers', 'UCLA', 'USC', 'Washington', 'Wisconsin']

PAC = ['Oregon State', 'Washington State']

# ranking big 12 schools from first to last based on current record 
# Ask user what they would like to know and answer the question using the ML model 
# use the team name to autofill Conference IE Florida is SEC no need to ask the user 

# Definition to return the current records per team
def get_singleTeamRec_data(year, team, confer, key):
  url = f'https://api.collegefootballdata.com/records?year={year}&team={team}&conference={confer}'
  headers = {'Authorization': f'{key}'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    return response.json()
  else:
    print(f'Error: {response.status_code}')
    return None

# Definition to return the current records per conference 
def get_specificConference_data(year, confer, key):
  url = f'https://api.collegefootballdata.com/records?year={year}&conference={confer}'
  headers = {'Authorization': f'{key}'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    return response.json()
  else:
    print(f'Error: {response.status_code}')
    return None

# Definition to return all team records
def get_allTeamRec_data(year, key):
  url = f'https://api.collegefootballdata.com/records?year={year}'
  headers = {'Authorization': f'{key}'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    return response.json()
  else:
    print(f'Error: {response.status_code}')
    return None
  

def get_talent(year, key):
  url = f'https://api.collegefootballdata.com/talent?year={year}'
  headers = {'Authorization': f'{key}'}  
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
      return response.json()
  else:
      print(f'Error: {response.status_code}')
      return None
    
# Definition to return the games' information per team
def get_specificGame_data(year, seasonType, team, key):
  url = f'https://api.collegefootballdata.com/games/teams?year={year}&seasonType={seasonType}&team={team}'
  headers = {'Authorization': f'{key}'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    return response.json()
  else:
    print(f'Error: {response.status_code}')
    return None

# Definition to return the talent scores per team
def retrieve_team_info(records):
    team_info = {}

    for record in records:
        team_name = record['team']
        team_expWins = record['expectedWins']
        team_totalWins = record['total']
        team_confGms = record['conferenceGames']
        team_homeGms = record['homeGames']
        team_awayGms = record['awayGames']
        # conferenceGames = get total conference games
        # total P4 conference games
        # other out of P4 conference games

        # Create a dictionary with the relevant data
        team_info = {
            'team': team_name,
            'expectedWins': team_expWins,
            'totalGames': {
                'wins': team_totalWins['wins'],
                'losses': team_totalWins['losses']
            },
            'conferenceGames': {
                'wins': team_confGms['wins'],
                'losses': team_confGms['losses']
            },
            'homeGames': {
                'wins': team_homeGms['wins'],
                'losses': team_homeGms['losses']
            },
            'awayGames': {
                'wins': team_awayGms['wins'],
                'losses': team_awayGms['losses']
            }
        }
    return team_info

def retrieve_conf_info(records):
    for record in records['teams']:
        team_name = record['school']
        team_points = record['points']
        
        # Initialize a dictionary to hold stats
        stats = {
            'rushingTDs': 0,
            'puntReturnYards': 0,
            'puntReturns': 0,
            'passingTDs': 0,
            'kickReturnYards': 0,
            'kickReturns': 0,
            'kickingPoints': 0,
            'tacklesForLoss': 0,
            'defensiveTDs': 0,
            'tackles': 0,
            'sacks': 0,
            'qbHurries': 0,
            'passesDeflected': 0,
            'possessionTime': 0,
            'interceptions': 0,
            'turnovers': 0,
            'totalPenaltiesYards': 0,
            'yardsPerRushAttempt': 0,
            'rushingAttempts': 0,
            'rushingYards': 0,
            'yardsPerPass': 0,
            'completionAttempts': 0,
            'netPassingYards': 0,
            'totalYards': 0,
            'fourthDownEffects': 0,
            'thirdDownEffects': 0,
            'firstDowns': 0,
        }

        for info in record['stats']:
            category = info['category']
            stat = info['stat']
            if category in stats:
                stats[category] = stat
        
        # Append the team info along with its stats
        return {
            'team_name' : team_name,
            'team_points': team_points,
            'rushingTDs': stats['rushingTDs'],
            'puntReturnYards': stats['puntReturnYards'],
            'puntReturns': stats['puntReturns'],
            'passingTDs': stats['passingTDs'],
            'kickReturnYards': stats['kickReturnYards'],
            'kickReturns': stats['kickReturns'],
            'kickingPoints': stats['kickingPoints'],
            'tacklesForLoss': stats['tacklesForLoss'],
            'defensiveTDs': stats['defensiveTDs'],
            'tackles': stats['tackles'],
            'sacks': stats['sacks'],
            'qbHurries': stats['qbHurries'],
            'passesDeflected': stats['passesDeflected'],
            'possessionTime': stats['possessionTime'],
            'interceptions': stats['interceptions'],
            'turnovers': stats['turnovers'],
            'totalPenaltiesYards': stats['totalPenaltiesYards'],
            'yardsPerRushAttempt': stats['yardsPerRushAttempt'],
            'rushingAttempts': stats['rushingAttempts'],
            'rushingYards': stats['rushingYards'],
            'yardsPerPass': stats['yardsPerPass'],
            'completionAttempts': stats['completionAttempts'],
            'netPassingYards': stats['netPassingYards'],
            'totalYards': stats['totalYards'],
            'fourthDownEffects': stats['fourthDownEffects'],
            'thirdDownEffects': stats['thirdDownEffects'],
            'firstDowns': stats['firstDowns']
        }

# Specific Conference will be an array of dictionaries

# power ranking
def team_power_rank(year):
  talents = get_talent(year)
  for talent in talents:
    if talent['school'] == team:
      return talent['talent'] # 746.30 Expected
  else:
   return "No Rating Found"

apiKey = str(input("Enter your API key: "))

year = 2024
seasonType = "regular"
team = 'UCF'
# team = str(input("Enter a team: "))

confer = "B12" # confer = str(input("Enter a conference: "))


# Talent Score *********************************
# talentScore = team_power_rank(year, confer)

organizedTeamInfo = []
seasonGameData = get_specificGame_data(year, seasonType, team, apiKey)
# print(seasonGameData)

for game in seasonGameData:
  gameInfo = retrieve_conf_info(game)
  if gameInfo['team_name'] == team:
    organizedTeamInfo.append(gameInfo)

# print(organizedTeamInfo)


organizedConfRecs = []
specificConferenceRec = get_specificConference_data(year, confer, apiKey)

# Traverse through specificConferenceRec and store in organizedConfRecs
for teamData in specificConferenceRec:
    teamInfo = retrieve_team_info([teamData])
    organizedConfRecs.append(teamInfo)

# sorted by total wins:
# sorted() sorts in ascending order
# key = lambda x: x['totalGames']['wins'] where lambda is a an anonymous function that will be used to sort by the wins
# reverse = True will sort in descending order

# *****************************************************
# organizedConfRecs = sorted(organizedConfRecs, key=lambda x: (x['totalGames']['wins'], x['totalGames']['losses']), reverse=True)
# for team in organizedConfRecs:
  # print(team['team'] + ": " + str(team['totalGames']['wins']) + "-" + str(team['totalGames']['losses']))

# Put this data into a .csv

with open('conferenceData.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Team', 'Expected Wins', 'Total Wins', 'Total Losses', 'Conference Wins', 'Conference Losses', 
                     'Home Wins', 'Home Losses', 'Away Wins', 'Away Losses'])

    for team in organizedConfRecs:
        writer.writerow([
            team['team'],                          # Team name
            team['expectedWins'],                  # Expected Wins
            team['totalGames']['wins'],            # Total Wins
            team['totalGames']['losses'],          # Total Losses
            team['conferenceGames']['wins'],       # Conference Wins
            team['conferenceGames']['losses'],     # Conference Losses
            team['homeGames']['wins'],             # Home Wins
            team['homeGames']['losses'],           # Home Losses
            team['awayGames']['wins'],             # Away Wins
            team['awayGames']['losses']            # Away Losses
        ])

with open('teamData.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow(['Team Name', 'Team Points', 'Rushing TDs', 'Punt Return Yards', 'Punt Returns', 'Passing TDs', 
                     'Kick Return Yards', 'Kick Returns', 'Kicking Points', 'Tackles For Loss',
                     'Defensive TDs', 'Tackles', 'Sacks', 'QB Hurries', 'Passes Deflected', 'Possession Time', 'Interceptions', 
                     'Turnovers', 'Total Penalties Yards', 'Yards Per Rush Attempt', 'Rushing Attempts', 'Rushing Yards', 
                     'Yards Per Pass', 'Completion Attempts', 'Net Passing Yards', 'Total Yards', 'Fourth Down Effects', 
                     'Third Down Effects', 'First Downs'])
    for team in organizedTeamInfo:
        writer.writerow([
          team['team_name'],
          team['team_points'],
          team['rushingTDs'],
          team['puntReturnYards'],
          team['puntReturns'],
          team['passingTDs'],
          team['kickReturnYards'],
          team['kickReturns'],
          team['kickingPoints'],
          team['tacklesForLoss'],
          team['defensiveTDs'],
          team['tackles'],
          team['sacks'],
          team['qbHurries'],
          team['passesDeflected'],
          team['possessionTime'],
          team['interceptions'],
          team['turnovers'],
          team['totalPenaltiesYards'],
          team['yardsPerRushAttempt'],
          team['rushingAttempts'],
          team['rushingYards'],
          team['yardsPerPass'],
          team['completionAttempts'],
          team['netPassingYards'],
          team['totalYards'],
          team['fourthDownEffects'],
          team['thirdDownEffects'],
          team['firstDowns']
        ])