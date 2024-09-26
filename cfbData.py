import requests
import csv

# *~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~*
# What to add next: 
# for loop that would make a new list of the teams based on the conference the user inputs ** DONE ** 
  # Add a function to rank the teams based on the current record
  # Add a function to rank the teams based on the expected record
# lets store each conference in a separate file and/or list so we dont have to continuosly call the API
# start the code for the machine learning - figure out what parameters with weights and algos we want to use
# *~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~**~~~*~~~*~~~*~~~*

# Predictor for Conference Winner
# which data to pull from
# use record to be able to predict Match ups

""" 
API Calls to Use: 
- /records
- /games
- /talent
- /
- /
- /
- /
- /

"""

# Steps to run: 

"""
1. Open the API 
2. Use the API Key to retrive the data
3. Come up with algo to predict the heisman 

Questions: 
How to use the API 
import requests

api.collegefootballdata.com/calendar
"""

"""
Template for pulling the Conferences/Using the API
def get_conferences_data():
    url = f'https://api.collegefootballdata.com/records?'
  headers = {'Authorization': f'{key}'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    return response.json()
  else:
    print(f'Error: {response.status_code}')
    return None



conferences = get_conferences_data()
print(conferences)
"""

# parameters = year, team, conferences 
# example: year = 2024, team = 'UCF', conference = B12
# print out only

"""
def get_records_data(year, team, confer):
    url = f'https://api.collegefootballdata.com/records?team={team}&conference={confer}'
  headers = {'Authorization': f'{key}'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    return response.json()
  else:
    print(f'Error: {response.status_code}')
    return None


year = int(input("Enter the year: "))
team = str(input("Enter the team: "))
confer = str(input("Enter the conference: "))

records = get_records_data(year, team, confer)

print(records)
"""

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
  
    
# Definition to return the talent scores per team
import requests

def get_talent(year, key):
  url = f'https://api.collegefootballdata.com/talent?year={year}'
  headers = {'Authorization': f'{key}'}  # Assuming 'Bearer' is needed
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
      return response.json()
  else:
      print(f'Error: {response.status_code}')
      return None

# Definition to sort the team records per team
def retrieve_team_info(records):
    team_info = {}

    for record in records:
        team_name = record['team']
        team_expWins = record['expectedWins']
        team_totalWins = record['total']
        team_confGms = record['conferenceGames']
        team_homeGms = record['homeGames']
        team_awayGms = record['awayGames']
        
        # Populate the team_info dictionary with the structured data
        team_info[team_name] = {
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

    # team_info[1] = team_expWins
    # team_info[2] = team_totalWins
    # team_info[3] = team_confGms
    # team_info[4] = team_homeGms
    # team_info[5] = team_awayGms
    

# power ranking
def team_power_rank(year, team):
  talents = get_talent(year)
  for talent in talents:
    if talent['school'] == team:
      return talent['talent'] # 746.30 Expected
  else:
   return "No Rating Found"

apiKey = str(input("Enter your API key: "))

year = 2024
#team = str(input("Enter a team: "))
confer = str(input("Enter a conference: "))

# Talent Score
# currentTalent = team_power_rank(year, team)

# Specific Team Record
# oneTeamRec = get_singleTeamRec_data(year, team, confer)

# Newly Sorted
# newRecords = retrieve_team_info(oneTeamRec)



# Specific Conference Record
# make organizedConfRecs an array of dictionaries that would store the conf info that we pull from this function

"""
Conference = Big 12
conferData [{}, {}, {}, {}, {}] -> Array of Dictionaries

conferData = [UCF, Colorado, Houston, Baylor, Utah] -> [0, 1, 2, 3, 4]
conferData[0] = {'school' = UCF, 'record' = 3-0-0'...}
conferData[example] = {'school' = example, 'record' = 0-0-0'...}

"""

# Specific Conference Call
# organizedConfRecs will be an array of dictionaries
organizedConfRecs = []
# Specific Conference will be an array of dictionaries
specificConferenceRec = get_specificConference_data(year, confer, apiKey)
# traverse through specificConferenceRec and store in organizedConfRecs
for teamData in specificConferenceRec:
  teamInfo = retrieve_team_info([teamData])
  organizedConfRecs.append(teamInfo)
# print(organizedConfRecs)

# Put this data into a .csv
with open('conferenceData.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Team', 'Expected Wins', 'Total Wins', 'Total Losses', 
                     'Conference Wins', 'Conference Losses', 
                     'Home Wins', 'Home Losses', 
                     'Away Wins', 'Away Losses'])
    
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


# Rank the teams based on their current record

# newRecords = sorted(organizedConfRecs, key=lambda x: x[2], reverse=True)
# print(newRecords)

# for team in organizedConfRecs:
#   print(team[0], team[2])


# print(organizedConfRecs[0][0])
# print(organizedConfRecs[0][2])

# All Team Records Call
# organizedRecs = []
# # Specific Conference will be an array of dictionaries
# specificRec = get_allTeamRec_data(year)
# # traverse through specificConferenceRec and store in organizedConfRecs
# for teamData in specificRec:
#   teamInfo = retrieve_team_info([teamData])
#   organizedRecs.append(teamInfo)
# print(organizedRecs)


# allTeamsRec = get_allTeamRec_data(year)
