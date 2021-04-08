import pandas as pd
import numpy as np
import datetime
from ELO import Club
from functions import teamELO, getTeamStats, getTeamLastStats
    

#Downloading football results from 2017-now
d20_21 = pd.read_csv("https://www.football-data.co.uk/mmz4281/2021/E0.csv", parse_dates=['Date'])
d19_20 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1920/E0.csv", parse_dates=['Date'])
d18_19 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1819/E0.csv", parse_dates=['Date'])
d17_18 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1718/E0.csv", parse_dates=['Date'])
d16_17 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1617/E0.csv", parse_dates=['Date'])
d15_16 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1516/E0.csv", parse_dates=['Date'])
d14_15 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1415/E0.csv", parse_dates=['Date'])

#Connecting dataframes into one dataframe
#data = pd.concat([d20_21])
dataStats = pd.concat([d20_21,d19_20,d18_19,d17_18])

#Sorting matches by date in ascending order
d20_21.sort_values(by='Date', ascending=True, inplace=True)
dataStats.sort_values(by='Date', ascending=True, inplace=True)

#Adding column with result for home and away team
hpts = []
apts = []
for i in range(dataStats.shape[0]):
    if(dataStats.iloc[i]['FTHG'] > dataStats.iloc[i]['FTAG']):
        hpts.append(1)
        apts.append(0)
    elif(dataStats.iloc[i]['FTHG'] == dataStats.iloc[i]['FTAG']):
        hpts.append(0.5)
        apts.append(0.5)
    else:
        hpts.append(0)
        apts.append(1)
        
dataStats['HPTS'] = hpts
dataStats['APTS'] = apts

#Making class Club instance for each club
clubsList = dataStats['HomeTeam'].unique()
clubs = {club: Club(name=club) for club in clubsList}

l = np.empty(d20_21.shape[0])
l.fill(0)
stats = pd.DataFrame({'homeShots':l,'homeShotsAgs':l,
                      'homeShotsTarget':l,'homeShotsTargetAgs':l,'homeCorners':l,
                      'homeCornersAgs':l,'last3homeShots':l,'last3homeShotsAgs':l,
                      'last3homeShotsTarget':l,'last3homeShotsTargetAgs':l,
                      'last3homeCorners':l,'last3homeCornersAgs':l,
                      'awayShots':l,'awayShotsAgs':l,
                      'awayShotsTarget':l,'awayShotsTargetAgs':l,'awayCorners':l,
                      'awayCornersAgs':l,'last3awayShots':l,'last3awayShotsAgs':l,
                      'last3awayShotsTarget':l,'last3awayShotsTargetAgs':l,
                      'last3awayCorners':l,'last3awayCornersAgs':l,'homeELO':l,
                      'awayELO':l})


hteams = []
ateams = []
dates = []
hgoals = []
agoals = []
for i in range(d20_21.shape[0]):
    hTeam = d20_21.iloc[i]['HomeTeam']
    aTeam = d20_21.iloc[i]['AwayTeam']
    date = d20_21.iloc[i]['Date']
    
    hgoals.append(d20_21.iloc[i]['FTHG'])
    agoals.append(d20_21.iloc[i]['FTAG'])
    
    #Generating stats
    hStats = getTeamStats(hTeam, dataStats, date)
    hLastStats = getTeamLastStats(hTeam, dataStats, date)
    aStats = getTeamStats(aTeam, dataStats, date)
    aLastStats = getTeamLastStats(aTeam, dataStats, date)
    eloRanking = teamELO(hTeam, aTeam, dataStats, date)
    #Assigning stats to dataframe
    hteams.append(hTeam)
    ateams.append(aTeam)
    dates.append(date)
    stats.iloc[i]['homeShots'] = hStats.iloc[0,1]
    stats.iloc[i]['homeShotsAgs'] = hStats.iloc[0,2]
    stats.iloc[i]['homeShotsTarget'] = hStats.iloc[0,3]
    stats.iloc[i]['homeShotsTargetAgs'] = hStats.iloc[0,4]
    stats.iloc[i]['homeCorners'] = hStats.iloc[0,5]
    stats.iloc[i]['homeCornersAgs'] = hStats.iloc[0,6]
    stats.iloc[i]['last3homeShots'] = hLastStats.iloc[0,1]
    stats.iloc[i]['last3homeShotsAgs'] = hLastStats.iloc[0,2]
    stats.iloc[i]['last3homeShotsTarget'] = hLastStats.iloc[0,3]
    stats.iloc[i]['last3homeShotsTargetAgs'] = hLastStats.iloc[0,4]
    stats.iloc[i]['last3homeCorners'] = hLastStats.iloc[0,5]
    stats.iloc[i]['last3homeCornersAgs'] = hLastStats.iloc[0,6]
    stats.iloc[i]['awayShots'] = aStats.iloc[0,1]
    stats.iloc[i]['awayShotsAgs'] = aStats.iloc[0,2]
    stats.iloc[i]['awayShotsTarget'] = aStats.iloc[0,3]
    stats.iloc[i]['awayShotsTargetAgs'] = aStats.iloc[0,4]
    stats.iloc[i]['awayCorners'] = aStats.iloc[0,5]
    stats.iloc[i]['awayCornersAgs'] = aStats.iloc[0,6]
    stats.iloc[i]['last3awayShots'] = aLastStats.iloc[0,1]
    stats.iloc[i]['last3awayShotsAgs'] = aLastStats.iloc[0,2]
    stats.iloc[i]['last3awayShotsTarget'] = aLastStats.iloc[0,3]
    stats.iloc[i]['last3awayShotsTargetAgs'] = aLastStats.iloc[0,4]
    stats.iloc[i]['last3awayCorners'] = aLastStats.iloc[0,5]
    stats.iloc[i]['last3awayCornersAgs'] = aLastStats.iloc[0,6]
    stats.iloc[i]['homeELO'] = eloRanking[hTeam].points
    stats.iloc[i]['awayELO'] = eloRanking[aTeam].points
    print(i)
      
stats['HomeTeam'] = hteams
stats['AwayTeam'] = ateams
stats['Date'] = dates
#Assigning target values
stats['HGoals'] = hgoals
stats['AGoals'] = agoals

stats.to_csv('stats.csv', index=False)
