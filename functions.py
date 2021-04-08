# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 18:08:58 2021

@author: Maciek
"""

import pandas as pd
import datetime
from ELO import Club

def teamELO(homeTeam, awayTeam, df, date):
    """
    Calculates homeTeam and awayTeam ELO ranking.

    Parameters
    ----------
    homeTeam : string
        The name of home team.
    awayTeam : string
        The name of away team.
    df : Pandas dataframe
        The data frame with information about matches.
    date : datetime
        The date of match between homeTeam and awayTeam.

    Returns
    -------
    clubs : dictionary
        The dictionary with all clubs ELO for three years from date.

    """
    #All clubs list
    clubsList = df['HomeTeam'].unique()
    #Getting matches for 3 years from date
    lastDate = date - datetime.timedelta(days=3*365)
    dfR = df[df['Date'] > lastDate]
    dfR = df[df['Date'] < date]
    #Making dict for clubs ELO's
    clubs = {club: Club(name=club) for club in clubsList}
    #Calculating and updating ELO ranking
    for i in range(dfR.shape[0]):
        homeRes = dfR.iloc[i]['HPTS']
        awayRes = dfR.iloc[i]['APTS']
        clubs[dfR.iloc[i]['HomeTeam']].update_points(clubs[dfR.iloc[i]['AwayTeam']],homeRes,awayRes)
    return clubs

def getTeamStats(team, df, date):
    """
    Calculates team average stats.

    Parameters
    ----------
    team : string
        The name of team.
    df : pandas dataframe
        The data frame containing information about matches.
    date : datetime
        Team match date.

    Returns
    -------
    stats : pandas dataframe
        The data frame containing average team stats from last year.

    """
    #Getting matches for one year from date
    year = datetime.timedelta(365)
    lastDate = date - year
    dfR = df[df['Date'] > lastDate]
    dfR = df[df['Date'] < date]
    #Making dataframe for team stats
    stats = pd.DataFrame({'TeamName':[team],'shots':[0],'shotsAgs':[0],'shotsTarget':[0],
                          'shotsTargetAgs':[0],'corners':[0],'cornersAgs':[0]})
    matches = 0
    #Summing all team stats
    for i in range(dfR.shape[0]):
        if(dfR.iloc[i]['HomeTeam']==team):
            stats['shots'] += dfR.iloc[i]['HS']
            stats['shotsAgs'] += dfR.iloc[i]['AS']
            stats['shotsTarget'] += dfR.iloc[i]['HST']
            stats['shotsTargetAgs'] += dfR.iloc[i]['AST']
            stats['corners'] += dfR.iloc[i]['HC']
            stats['cornersAgs'] += dfR.iloc[i]['AC']
            matches += 1
        elif(dfR.iloc[i]['AwayTeam']==team):
            stats['shots'] += dfR.iloc[i]['AS']
            stats['shotsAgs'] += dfR.iloc[i]['HS']
            stats['shotsTarget'] += dfR.iloc[i]['AST']
            stats['shotsTargetAgs'] += dfR.iloc[i]['HST']
            stats['corners'] += dfR.iloc[i]['AC']
            stats['cornersAgs'] += dfR.iloc[i]['HC']
            matches += 1
    #Calculating average team stats
    stats['shots'] /= matches
    stats['shotsAgs'] /= matches
    stats['shotsTarget'] /= matches
    stats['shotsTargetAgs'] /= matches
    stats['corners'] /= matches
    stats['cornersAgs'] /= matches
    
    return stats

def getTeamLastStats(team, df, date):
    """
    Calculate team average stats in last matches

    Parameters
    ----------
    team : string
        The name of team.
    df : pandas dataframe
        The data frame containing information about matches.
    date : datetime
        Team match date.

    Returns
    -------
    stats : pandas dataframe
        The data frame containing average team stats from last 3 games.

    """
    dfR = df[df['Date']< date]
    stats = pd.DataFrame({'TeamName':[team],'shots':[0],'shotsAgs':[0],'shotsTarget':[0],
                      'shotsTargetAgs':[0],'corners':[0],'cornersAgs':[0]})
    matches = 0
    for i in range(dfR.shape[0]):       
        if(dfR.iloc[i]['HomeTeam'] == team):
            if(matches == 3):
                break
            stats['shots'] += dfR.iloc[i]['HS']
            stats['shotsAgs'] += dfR.iloc[i]['AS']
            stats['shotsTarget'] += dfR.iloc[i]['HST']
            stats['shotsTargetAgs'] += dfR.iloc[i]['AST']
            stats['corners'] += dfR.iloc[i]['HC']
            stats['cornersAgs'] += dfR.iloc[i]['AC']
            matches += 1
        elif(dfR.iloc[i]['AwayTeam']==team):
            stats['shots'] += dfR.iloc[i]['AS']
            stats['shotsAgs'] += dfR.iloc[i]['HS']
            stats['shotsTarget'] += dfR.iloc[i]['AST']
            stats['shotsTargetAgs'] += dfR.iloc[i]['HST']
            stats['corners'] += dfR.iloc[i]['AC']
            stats['cornersAgs'] += dfR.iloc[i]['HC']
            matches += 1
    
    #Calculating average team stats
    stats['shots'] /= matches
    stats['shotsAgs'] /= matches
    stats['shotsTarget'] /= matches
    stats['shotsTargetAgs'] /= matches
    stats['corners'] /= matches
    stats['cornersAgs'] /= matches
    
    return stats

def make_table(df, hgcol, agcol, ht, at):
    """
    Returns the dictionary containing team names as values and amount 
    of points as values

    Parameters:
        df (DataFrame): the data frame with results of matches
        hgcol (string): the name of column with amount of home team goals
        agcol (string): the name of column with amount of away team goals
        ht (string): the name of column containing home teams
        at (string): the name of column containing away teams
    
    Returns:
        points (dictionary): the dictionary with team names as keys and amount 
        of points as value
    """
    hpts = []
    apts = []
    
    for i in range(df.shape[0]):
        if df.iloc[i][hgcol] > df.iloc[i][agcol]:
            hpts.append(3)
            apts.append(0)
        elif df.iloc[i][hgcol] < df.iloc[i][agcol]:
            hpts.append(0)
            apts.append(3)
        else:   
            hpts.append(1)
            apts.append(1)
            
    df['HPts'] = hpts
    df['APts'] = apts
    
    teamsNames = df[ht].unique()
    
    points = {}
    for team in teamsNames:
        points[team] = 0
    
    for team in teamsNames:
        for i in range(df.shape[0]):
            if(df.iloc[i][ht] == team):
                points[team] += df.iloc[i]['HPts']
            elif(df.iloc[i][at] == team):
                points[team] += df.iloc[i]['APts']
    
    return points