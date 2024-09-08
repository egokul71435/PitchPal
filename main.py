import discord
import os
from dotenv import load_dotenv
import requests
# to make http requests to get data from the api
import http.client
import json
import random
# to work with api data
from replit import db
from keep_bot_alive import keep_bot_alive
# for time management
from datetime import datetime
from dateutil import tz

load_dotenv()
client = discord.Client(intents=discord.Intents.default())
# init discord client with normal params

if 'responding' not in db.keys():
  db['responding'] = True
# to check if the bot is responding

def update_listofclubs(new_club, user_ID):
    if 'listofclubs' in db.keys():
        clubs = db['listofclubs']
        clubs.append({user_ID : new_club})
        db['listofclubs'] = clubs
    # add to existing list
    else:
        db['listofclubs'] = [{user_ID : new_club}]
    # create new list if empty

def delete_club(club_to_delete, user_ID):
    clubs = db['listofclubs']
    if {user_ID : club_to_delete} in clubs:
        clubs.remove({user_ID : club_to_delete})
        db['listofclubs'] = clubs
    

uri = 'https://api.football-data.org/v4/competitions/PL/matches?matchday=4'
headers = { 'X-Auth-Token': os.getenv('KEY') }
response = requests.get(uri, headers=headers)
print(response)
print(response.json())
# api testing

def get_standings():
    uri = 'http://api.football-data.org/v4/competitions/PL/standings'
    headers = { 'X-Auth-Token': os.getenv('KEY') }
    standings = requests.get(uri, headers=headers)
    json_data = json.loads(standings.text)
    result = []
    for i in range(len(json_data['standings'][0]['table'])):
        team = json_data['standings'][0]['table'][i]['team']['name']
        points = str(json_data['standings'][0]['table'][i]['points']) + ' points'
        position = (json_data['standings'][0]['table'][i]['position']) 
        result.append(f"{position} - {team} - {points}")
    return result
    
def get_stats():
    uri = 'https://api.football-data.org/v4/competitions/PL/scorers'
    headers = { 'X-Auth-Token': os.getenv('KEY') }
    stats = requests.get(uri, headers=headers)
    json_data = json.loads(stats.text)
    result = []
    for i in range(len(json_data['scorers'])):
        player = json_data['scorers'][i]['player']['name']
        goals = str(json_data['scorers'][i]['goals']) + ' goals'
        assists = str(json_data['scorers'][i]['assists']) + ' assists'
        result.append(f"{player} - {goals} - {assists}")
    return result

def get_matchday():
    uri = 'http://api.football-data.org/v4/competitions/PL/standings'
    headers = { 'X-Auth-Token': os.getenv('KEY') }
    standings = requests.get(uri, headers=headers)
    json_data = json.loads(standings.text)
    return int(json_data['season']['currentMatchday'])+1


def get_fixtures():
    matchday = get_matchday()
    uri = 'https://api.football-data.org/v4/competitions/PL/matches?matchday=' + str(matchday)
    headers = { 'X-Auth-Token': os.getenv('KEY') }
    fixtures = requests.get(uri, headers=headers)
    json_data = json.loads(fixtures.text)
    matches = []
    for i in range(len(json_data['matches'])):
        home = json_data['matches'][i]['homeTeam']['name']
        away = json_data['matches'][i]['awayTeam']['name']
        time = json_data['matches'][i]['utcDate']
        matches.append(f"{home} vs {away} at {time}")
    return matches

def data_get_fixtures():
    matchday = get_matchday()
    uri = 'https://api.football-data.org/v4/competitions/PL/matches?matchday=' + str(matchday)
    headers = { 'X-Auth-Token': os.getenv('KEY') }
    fixtures = requests.get(uri, headers=headers)
    json_data = json.loads(fixtures.text)
    matches = []
    for i in range(len(json_data['matches'])):
        datapoint = []
        home = json_data['matches'][i]['homeTeam']['name']
        datapoint.append(home)
        away = json_data['matches'][i]['awayTeam']['name']
        datapoint.append(away)
        time = json_data['matches'][i]['utcDate']
        datapoint.append(time)
        matches.append(datapoint)
    return matches


@client.event
async def on_ready():
  print('logged in as {0.user}'.format(client))
# bot ready message on console

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # if message is from bot, ignore
    if message.content.startswith('!standings'):
        standings = get_standings()
        for i in range(len(standings)):
            await message.channel.send(standings[i])
    if message.content.startswith('!stats'):
        stats = get_stats()
        for i in range(len(stats)):
            await message.channel.send(stats[i])
    if message.content.startswith('!fixtures'):
        fixtures = get_fixtures()
        for i in range(len(fixtures)):
            await message.channel.send(fixtures[i])
    if message.content.startswith('!addclub'):
        club = message.content.split('!addclub ',1)[1]
        update_listofclubs(club, message.author.id)
        await message.channel.send('club has been stored')
    if message.content.startswith('!deleteclub'):
        club = message.content.split('!deleteclub ',1)[1]
        #clubs = []
        if 'listofclubs' in db.keys():
            
            delete_club(club, message.author.id)
            #clubs = db['listofclubs']
        await message.channel.send('club has been deleted')
        

keep_bot_alive()
client.run(os.getenv('TOKEN'))