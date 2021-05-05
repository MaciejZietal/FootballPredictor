import pandas as pd
import numpy as np
from ELO import Club
from functions import teamELO, getHomeTeamStats, getAwayTeamStats, getTeamLastStats
    
#Reading data
d20_21 = pd.read_csv('data/d20_21.csv')
d19_20 = pd.read_csv('data/d19_20.csv')
d18_19 = pd.read_csv('data/d18_19.csv')
d17_18 = pd.read_csv('data/d17_18.csv')
d16_17 = pd.read_csv('data/d16_17.csv')
d15_16 = pd.read_csv('data/d15_16.csv')
d14_15 = pd.read_csv('data/d14_15.csv')

#Connecting dataframes into one dataframe 
dataStats = pd.concat([d19_20,d18_19,d17_18,d16_17,d15_16,d14_15])
learningStats = pd.concat([d19_20,d18_19])

#Reversing dataframes
dataStats = dataStats.iloc[::-1]
learningStats = learningStats.iloc[::-1]

#Setting rigth type of date
learningStats['Date']=pd.to_datetime(learningStats['Date'])
dataStats['Date']=pd.to_datetime(dataStats['Date'])

#Adding column with result for home and away team
ehpts = []
eapts = []
hpts = []
apts = []
for i in range(dataStats.shape[0]):
    if(dataStats.iloc[i]['FTHG'] > dataStats.iloc[i]['FTAG']):
        ehpts.append(1)
        hpts.append(3)
        eapts.append(0)
        apts.append(0)
    elif(dataStats.iloc[i]['FTHG'] == dataStats.iloc[i]['FTAG']):
        ehpts.append(0.5)
        hpts.append(1)
        eapts.append(0.5)
        apts.append(1)
    else:
        ehpts.append(0)
        hpts.append(0)
        eapts.append(1)
        apts.append(3)
        
dataStats['ELOHPTS'] = ehpts
dataStats['ELOAPTS'] = eapts
dataStats['HPTS'] = hpts
dataStats['APTS'] = apts

#Making class Club instance for each club
clubsList = dataStats['HomeTeam'].unique()
clubs = {club: Club(name=club) for club in clubsList}

l = np.empty(learningStats.shape[0])
l.fill(0)
stats = pd.DataFrame({'homeGoals':l,'homeGoalsAgs':l,
                      'homeGoalsStd':l,'homeGoalsAgsStd':l,'last5homeGoals':l,
                      'last5homeGoalsAgs':l,'last5homePointsPerc':l,'homeELO':l,
                      'awayGoals':l,'awayGoalsAgs':l,
                      'awayGoalsStd':l,'awayGoalsAgsStd':l,'last5awayGoals':l,
                      'last5awayGoalsAgs':l,'last5awayPointsPerc':l,'awayELO':l
                      })


hteams = []
ateams = []
dates = []
hgoals = []
agoals = []
for i in range(learningStats.shape[0]):
    hTeam = learningStats.iloc[i]['HomeTeam']
    aTeam = learningStats.iloc[i]['AwayTeam']
    date = learningStats.iloc[i]['Date']
    
    hgoals.append(learningStats.iloc[i]['FTHG'])
    agoals.append(learningStats.iloc[i]['FTAG'])
    
    #Generating stats
    hStats = getHomeTeamStats(hTeam, dataStats, date)
    hLastStats = getTeamLastStats(hTeam, dataStats, date)
    aStats = getAwayTeamStats(aTeam, dataStats, date)
    aLastStats = getTeamLastStats(aTeam, dataStats, date)
    eloRanking = teamELO(hTeam, aTeam, dataStats, date)
    #Assigning stats to dataframe
    hteams.append(hTeam)
    ateams.append(aTeam)
    dates.append(date)
    stats.iloc[i]['homeGoals'] = hStats.iloc[0,1]
    stats.iloc[i]['homeGoalsAgs'] = hStats.iloc[0,2]
    stats.iloc[i]['homeGoalsStd'] = hStats.iloc[0,3]
    stats.iloc[i]['homeGoalsAgsStd'] = hStats.iloc[0,4]
    stats.iloc[i]['last5homeGoals'] = hLastStats.iloc[0,1]
    stats.iloc[i]['last5homeGoalsAgs'] = hLastStats.iloc[0,2]
    stats.iloc[i]['last5homePointsPerc'] = hLastStats.iloc[0,3]
    stats.iloc[i]['homeELO'] = eloRanking[hTeam].points
    
    stats.iloc[i]['awayGoals'] = aStats.iloc[0,1]
    stats.iloc[i]['awayGoalsAgs'] = aStats.iloc[0,2]
    stats.iloc[i]['awayGoalsStd'] = aStats.iloc[0,3]
    stats.iloc[i]['awayGoalsAgsStd'] = aStats.iloc[0,4]
    stats.iloc[i]['last5awayGoals'] = aLastStats.iloc[0,1]
    stats.iloc[i]['last5awayGoalsAgs'] = aLastStats.iloc[0,2]
    stats.iloc[i]['last5awayPointsPerc'] = aLastStats.iloc[0,3]
    stats.iloc[i]['awayELO'] = eloRanking[aTeam].points
    print(i)
      
stats['HomeTeam'] = hteams
stats['AwayTeam'] = ateams
stats['Date'] = dates
#Assigning target values
stats['HGoals'] = hgoals
stats['AGoals'] = agoals

stats.to_csv('data/stats.csv', index=False)
