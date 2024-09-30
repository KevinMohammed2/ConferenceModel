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


# parameters = year, team, conferences 
# example: year = 2024, team = 'UCF', conference = B12
# print out only


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


# Specific Conference will be an array of dictionaries

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
# team = str(input("Enter a team: "))
confer = str(input("Enter a conference: "))

# Talent Score
# currentTalent = team_power_rank(year, team)

# Specific Team Record
# oneTeamRec = get_singleTeamRec_data(year, team, confer)

# Newly Sorted
# newRecords = retrieve_team_info(oneTeamRec)

# Specific Conference Record
# make organizedConfRecs an array of dictionaries that would store the conf info that we pull from this function


organizedConfRecs = []
specificConferenceRec = get_specificConference_data(year, confer, apiKey)

# Traverse through specificConferenceRec and store in organizedConfRecs
for teamData in specificConferenceRec:
    teamInfo = retrieve_team_info([teamData])
    organizedConfRecs.append(teamInfo)
    
print(organizedConfRecs)


# sorted by total wins:
# sorted() sorts in ascending order
# key = lambda x: x['totalGames']['wins'] where lambda is a an anonymous function that will be used to sort by the wins
# reverse = True will sort in descending order
organizedConfRecs = sorted(organizedConfRecs, key=lambda x: (x['totalGames']['wins'], x['totalGames']['losses']), reverse=True)
for team in organizedConfRecs:
  print(team['team'] + ": " + str(team['totalGames']['wins']) + "-" + str(team['totalGames']['losses']))

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

# Newest Changes

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
