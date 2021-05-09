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
        homeRes = dfR.iloc[i]['ELOHPTS']
        awayRes = dfR.iloc[i]['ELOAPTS']
        clubs[dfR.iloc[i]['HomeTeam']].update_points(clubs[dfR.iloc[i]['AwayTeam']],homeRes,awayRes)
    return clubs

def getHomeTeamStats(team, df, date):
    """
    Calculates team average stats at home.

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
        The data frame containing average team stats at home from last year.

    """
    #Getting matches for one year from date
    year = datetime.timedelta(365)
    lastDate = date - year
    dfR = df[df['Date'] > lastDate]
    dfR = df[df['Date'] < date]
    #Making dataframe for team stats
    stats = pd.DataFrame({'TeamName':[team],'goals':[0],'goalsAgs':[0],'goalsStd':[0],
                          'goalsAgsStd':[0]})

    #Calculating stats
    hteam = dfR[dfR['HomeTeam']==team]
    stats['goals'] = hteam['FTHG'].mean()
    stats['goalsAgs'] = hteam['FTAG'].mean()
    stats['goalsStd'] = hteam['FTHG'].std()
    stats['goalsAgsStd'] = hteam['FTAG'].std()
    
    return stats

def getAwayTeamStats(team, df, date):
    """
    Calculates team average stats from away matches.

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
        The data frame containing average team stats from away matches from last year.

    """
    #Getting matches for one year from date
    year = datetime.timedelta(365)
    lastDate = date - year
    dfR = df[df['Date'] > lastDate]
    dfR = df[df['Date'] < date]
    #Making dataframe for team stats
    stats = pd.DataFrame({'TeamName':[team],'goals':[0],'goalsAgs':[0],'goalsStd':[0],
                          'goalsAgsStd':[0]})

    #Calculating stats
    hteam = dfR[dfR['AwayTeam']==team]
    stats['goals'] = hteam['FTAG'].mean()
    stats['goalsAgs'] = hteam['FTHG'].mean()
    stats['goalsStd'] = hteam['FTAG'].std()
    stats['goalsAgsStd'] = hteam['FTHG'].std()
    
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
    stats = pd.DataFrame({'TeamName':[team],'goals':[0],'goalsAgs':[0],'pointsPer':[0]})
    d = dfR[(dfR['HomeTeam']==team) | (dfR['AwayTeam']==team)]
    d=d.iloc[:5]
    
    #Calculating average team stats
    for i in range(d.shape[0]):
        if(d.iloc[i]['HomeTeam']==team):
            stats['goals'] += d.iloc[i]['FTHG']
            stats['goalsAgs'] += d.iloc[i]['FTAG']
            stats['pointsPer'] += d.iloc[i]['HPTS']
        else:
            stats['goals'] += d.iloc[i]['FTAG']
            stats['goalsAgs'] += d.iloc[i]['FTHG']
            stats['pointsPer'] += d.iloc[i]['APTS']
            
    stats['goals'] /= d.shape[0]
    stats['goalsAgs'] /= d.shape[0]
    stats['pointsPer'] /= d.shape[0]
    
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

def generateStats(df, homeTeam, awayTeam, date):
    
    hpts=[]
    apts=[]
    ehpts=[]
    eapts=[]
    for i in range(df.shape[0]):
        if df.iloc[i]['FTHG'] > df.iloc[i]['FTAG']:
            hpts.append(3)
            apts.append(1)
            ehpts.append(1)
            eapts.append(0)
        elif df.iloc[i]['FTHG'] < df.iloc[i]['FTAG']:
            hpts.append(0)
            apts.append(3)
            ehpts.append(0)
            eapts.append(1)
        else:   
            hpts.append(1)
            apts.append(1)
            ehpts.append(0.5)
            eapts.append(0.5)
    df['HPTS'] = hpts
    df['APTS'] = apts
    df['ELOHPTS'] = ehpts
    df['ELOAPTS'] = eapts
    
    stats = pd.DataFrame({'homeGoals':[0],'homeGoalsAgs':[0],
                      'homeGoalsStd':[0],'homeGoalsAgsStd':[0],'last5homeGoals':[0],
                      'last5homeGoalsAgs':[0],'last5homePointsPerc':[0],'homeELO':[0],
                      'awayGoals':[0],'awayGoalsAgs':[0],
                      'awayGoalsStd':[0],'awayGoalsAgsStd':[0],'last5awayGoals':[0],
                      'last5awayGoalsAgs':[0],'last5awayPointsPerc':[0],'awayELO':[0]
                      })
    
    hStats = getHomeTeamStats(homeTeam, df, date)
    hLastStats = getTeamLastStats(homeTeam, df, date)
    aStats = getAwayTeamStats(awayTeam, df, date)
    aLastStats = getTeamLastStats(awayTeam, df, date)
    eloRanking = teamELO(homeTeam, awayTeam, df, date)
    
    stats['homeGoals'] = hStats.iloc[0,1]
    stats['homeGoalsAgs'] = hStats.iloc[0,2]
    stats['homeGoalsStd'] = hStats.iloc[0,3]
    stats['homeGoalsAgsStd'] = hStats.iloc[0,4]
    stats['last5homeGoals'] = hLastStats.iloc[0,1]
    stats['last5homeGoalsAgs'] = hLastStats.iloc[0,2]
    stats['last5homePointsPerc'] = hLastStats.iloc[0,3]
    if(eloRanking.__contains__(homeTeam)):
        stats['homeELO'] = eloRanking[homeTeam].points
    else:
        stats['homeELO'] = 1000
    
    stats['awayGoals'] = aStats.iloc[0,1]
    stats['awayGoalsAgs'] = aStats.iloc[0,2]
    stats['awayGoalsStd'] = aStats.iloc[0,3]
    stats['awayGoalsAgsStd'] = aStats.iloc[0,4]
    stats['last5awayGoals'] = aLastStats.iloc[0,1]
    stats['last5awayGoalsAgs'] = aLastStats.iloc[0,2]
    stats['last5awayPointsPerc'] = aLastStats.iloc[0,3]
    if(eloRanking.__contains__(awayTeam)):
        stats['awayELO'] = eloRanking[awayTeam].points
    else:
        stats['awayELO'] = 1000
    
    return stats

def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result

def give_points(df,hg,ag):
    hpts = []
    apts = []
    for i in range(df.shape[0]):
        if(df.iloc[i][hg]>df.iloc[i][ag]):
            hpts.append(3)
            apts.append(0)
        elif(df.iloc[i][hg]<df.iloc[i][ag]):
            hpts.append(0)
            apts.append(3)
        else:
            hpts.append(1)
            apts.append(1)
            
    df['HPts'] = hpts
    df['APts'] = apts
    
    return df
