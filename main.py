import requests

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
  url = 'https://api.collegefootballdata.com/conferences'
  headers = {'Authorization': 
             'Bearer /PCWShwQUVu2KcOmIA0UoA/04MRAffVT0QG+3hb4m0g0Ug3txcvhnapqf1CuYOf2'}
  # Replace YOUR_API_KEY with your actual API key
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
  url = f'https://api.collegefootballdata.com/records?year={year}&team={team}&conference={confer}'
  headers = {'Authorization': 
   'Bearer /PCWShwQUVu2KcOmIA0UoA/04MRAffVT0QG+3hb4m0g0Ug3txcvhnapqf1CuYOf2'}
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

def get_currRec_data(year, team, confer):
  url = f'https://api.collegefootballdata.com/records?year={year}&team={team}&conference={confer}'
  headers = {'Authorization': 
   'Bearer /PCWShwQUVu2KcOmIA0UoA/04MRAffVT0QG+3hb4m0g0Ug3txcvhnapqf1CuYOf2'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    return response.json()
  else:
    print(f'Error: {response.status_code}')
    return None

def retrieve_team_info(records):
  team_info = {}
  #team_info = [0, 1, 2] => ['team', 'expWins', 'total']
  for record in records:
    team_name = record['team']
    team_expWins = record['expectedWins']
    team_totalWins = record['total']
    team_confGms = record['conferenceGames']
    team_homeGms = record['homeGames']
    team_awayGms = record['awayGames']
    
    team_info[0] = team_name
    team_info[1] = team_expWins
    team_info[2] = team_totalWins
    team_info[3] = team_confGms
    team_info[4] = team_homeGms
    team_info[5] = team_awayGms

  return team_info

year = 2024
team = str(input("Enter a team: "))
confer = str(input("Enter a conference: "))


records = get_currRec_data(year, team, confer)
newRecords = retrieve_team_info(records)

wins = newRecords[2]['wins']
losses = newRecords[2]['losses']
ties = newRecords[2]['ties']
expected_wins = newRecords[1]

print("record:", wins, '-', losses, '-', ties, 'expected wins:', expected_wins)

# what to add next: 
# for loop that would make a new list of the teams based on the conference the user inputs
  # Add a function to rank the teams based on the current record
  # Add a function to rank the teams based on the expected record
# lets store each conference in a separate file and/or list so we dont have to continuosly call the API
# start the code for the machine learning - figure out what parameters with weights and algos we want to use
