import pandas as pd
import datetime
from ELO import Club

def give_points(df, hGoals, aGoals):
    """
    Returns a dataframe with added columns with ammount of points for every match
    (3 for win, 1 for draw, 0 for loss).
    
    Parameters
    df : dataframe
        the data frame with results of matches.
    hGoals : string
        the name of column containing the ammount of home team goals.
    aGoals : string
        the name of column containing the ammount of away team goals.

    Returns:
        df (dataframe): the dataframe with added two columns hPts and aPts.

    """
    hpts = []
    apts = []
    for i in range(df.shape[0]):
        if(df.iloc[i][hGoals]>df.iloc[i][aGoals]):
            hpts.append(3)
            apts.append(0)
        elif(df.iloc[i][hGoals]<df.iloc[i][aGoals]):
            hpts.append(0)
            apts.append(3)
        else:
            hpts.append(1)
            apts.append(1)
            
    df['HPts'] = hpts
    df['APts'] = apts
    
    return df

def give_ELO_points(df, hGoals, aGoals):
    """
    Returns a dataframe with added columns with ammount of points for every match
    (1 for win, 0.5 for draw, 0 for loss)
    
    Parameters
    df : dataframe
        the data frame with results of matches.
    hGoals : string
        the name of column containing the ammount of home team goals.
    aGoals : string
        the name of column containing the ammount of away team goals.

    Returns:
        df (dataframe): the dataframe with added two columns hPts and aPts.

    """
    hpts = []
    apts = []
    for i in range(df.shape[0]):
        if(df.iloc[i][hGoals]>df.iloc[i][aGoals]):
            hpts.append(3)
            apts.append(0)
        elif(df.iloc[i][hGoals]<df.iloc[i][aGoals]):
            hpts.append(0)
            apts.append(3)
        else:
            hpts.append(1)
            apts.append(1)
            
    df['ELOHPts'] = hpts
    df['ELOAPts'] = apts
    
    return df    

def make_table(df, hgcol, agcol, ht, at):
    """
    Returns the dictionary containing team names as values and amount 
    of points as values

    Parameters:
        df : DataFrame
            the data frame with results of matches
        hgcol : string
            the name of column with amount of home team goals
        agcol : string
            the name of column with amount of away team goals
        ht : string
            the name of column containing home teams
        at : string
            the name of column containing away teams
    
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
        homeRes = dfR.iloc[i]['ELOHPts']
        awayRes = dfR.iloc[i]['ELOAPts']
        if(dfR.iloc[i]['HomeTeam'] not in clubs):
            clubs[dfR.iloc[i]['HomeTeam']] = Club(name=dfR.iloc[i]['HomeTeam'])
        if(dfR.iloc[i]['AwayTeam'] not in clubs):
            clubs[dfR.iloc[i]['AwayTeam']] = Club(name=dfR.iloc[i]['AwayTeam'])
        clubs[dfR.iloc[i]['HomeTeam']].update_points(clubs[dfR.iloc[i]['AwayTeam']],homeRes,awayRes)
    return clubs

def homeStats(team, df, date):
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
    lastDate = date - datetime.timedelta(days=365)
    df['Date'] = pd.to_datetime(df['Date'])
    dfR = df[df['Date'] > lastDate]
    dfR = df[df['Date'] < date]
    #Making dataframe for team stats
    stats = pd.DataFrame({'hGoals':[0],'hGoalsAgs':[0],'hShots':[0],'hShotsAgs':[0],
                          'hShotsTar':[0],'hShotsAgsTar':[0],'hCorners':[0],
                          'hCornersAgs':[0]})

    #Calculating stats
    hteam = dfR[dfR['HomeTeam']==team]
    stats['hGoals'] = hteam['FTHG'].mean()
    stats['hGoalsAgs'] = hteam['FTAG'].mean()
    stats['hShots'] = hteam['HS'].mean()
    stats['hShotsAgs'] = hteam['AS'].mean()
    stats['hShotsTar'] = hteam['HST'].mean()
    stats['hShotsAgsTar'] = hteam['AST'].mean()
    stats['hCorners'] = hteam['HC'].mean()
    stats['hCornersAgs'] = hteam['AC'].mean()
    
    return stats

def awayStats(team, df, date):
    """
    Calculates team average stats away.

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
        The data frame containing average team stats away from last year.

    """
    #Getting matches for one year from date
    year = datetime.timedelta(365)
    lastDate = date - year
    dfR = df[df['Date'] > lastDate]
    dfR = df[df['Date'] < date]
    #Making dataframe for team stats
    stats = pd.DataFrame({'aGoals':[0],'aGoalsAgs':[0],'aShots':[0],'aShotsAgs':[0],
                          'aShotsTar':[0],'aShotsAgsTar':[0],'aCorners':[0],
                          'aCornersAgs':[0]})

    #Calculating stats
    aTeam = dfR[dfR['HomeTeam']==team]
    stats['aGoals'] = aTeam['FTHG'].mean()
    stats['aGoalsAgs'] = aTeam['FTAG'].mean()
    stats['aShots'] = aTeam['HS'].mean()
    stats['aShotsAgs'] = aTeam['AS'].mean()
    stats['aShotsTar'] = aTeam['HST'].mean()
    stats['aShotsAgsTar'] = aTeam['AST'].mean()
    stats['aCorners'] = aTeam['HC'].mean()
    stats['aCornersAgs'] = aTeam['AC'].mean()
    
    return stats

def lastTeamStats(team, df, date, hteam=True):
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
    hteam : boolean
        True if this team is playing at home, False otherwise.

    Returns
    -------
    stats : pandas dataframe
        The data frame containing average team stats from last 3 games.

    """
    dfR = df[df['Date']< date]
    if(hteam):
        stats = pd.DataFrame({'hGoals':[0],'hGoalsAgs':[0],'hPointsAvg':[0],
                          'hShots':[0],'hShotsAgs':[0],'hShotsTar':[0],
                          'hShotsAgsTar':[0],'hCorners':[0],
                          'hCornersAgs':[0]})
    else:
        stats = pd.DataFrame({'aGoals':[0],'aGoalsAgs':[0],'aPointsAvg':[0],
                          'aShots':[0],'aShotsAgs':[0],'aShotsTar':[0],
                          'aShotsAgsTar':[0],'aCorners':[0],
                          'aCornersAgs':[0]})
    d = dfR[(dfR['HomeTeam']==team) | (dfR['AwayTeam']==team)]
    d=d.iloc[:5]
    
    #Calculating average team stats
    for i in range(d.shape[0]):
        if(d.iloc[i]['HomeTeam']==team):
            stats.iloc[:,0] += d.iloc[i]['FTHG']
            stats.iloc[:,1] += d.iloc[i]['FTAG']
            stats.iloc[:,2] += d.iloc[i]['HPts']
            stats.iloc[:,3] += d.iloc[i]['HS']
            stats.iloc[:,4] += d.iloc[i]['AS']
            stats.iloc[:,5] += d.iloc[i]['HST']
            stats.iloc[:,6] += d.iloc[i]['AST']
            stats.iloc[:,7] += d.iloc[i]['HC']
            stats.iloc[:,8] += d.iloc[i]['AC']
        else:
            stats.iloc[:,0] += d.iloc[i]['FTAG']
            stats.iloc[:,1] += d.iloc[i]['FTHG']
            stats.iloc[:,2] += d.iloc[i]['APts']
            stats.iloc[:,3] += d.iloc[i]['AS']
            stats.iloc[:,4] += d.iloc[i]['HS']
            stats.iloc[:,5] += d.iloc[i]['AST']
            stats.iloc[:,6] += d.iloc[i]['HST']
            stats.iloc[:,7] += d.iloc[i]['AC']
            stats.iloc[:,8] += d.iloc[i]['HC']
            
    stats.iloc[:,0] /= d.shape[0]
    stats.iloc[:,1] /= d.shape[0]
    stats.iloc[:,2] /= d.shape[0]
    stats.iloc[:,3] /= d.shape[0]
    stats.iloc[:,4] /= d.shape[0]
    stats.iloc[:,5] /= d.shape[0]
    stats.iloc[:,6] /= d.shape[0]
    stats.iloc[:,7] /= d.shape[0]
    stats.iloc[:,8] /= d.shape[0]
    
    return stats

def matchStats(hTeam, aTeam, df, date):
    """
    Calculates statistics for a match.

    Parameters
    ----------
    hTeam : string
        The name of home team.
    aTeam : string
        The name of away team.
    df : pandas dataframe
        The data frame containing information about matches.
    date : datetime
        Team match date.

    Returns
    -------
    stats : pandas dataframe
        The data frame containing average teams stats for the match.

    """
    df = give_ELO_points(df, 'FTHG','FTAG')
    df = give_points(df, 'FTHG', 'FTAG')
    
    hStats = homeStats(hTeam, df, date)
    aStats = awayStats(aTeam, df, date)
    hLastStats = lastTeamStats(hTeam, df, date)
    aLastStats = lastTeamStats(aTeam, df, date)
    stats = pd.concat([hStats,aStats, hLastStats, aLastStats],axis=1)
    elo = teamELO(hTeam, aTeam, df, date)
    if(elo.__contains__(hTeam)):
        stats['hELO'] = elo[hTeam].points
    else:
        stats['hELO'] = 1000
    if(elo.__contains__(aTeam)):
        stats['aELO'] = elo[aTeam].points
    else:
        stats['aELO'] = 1000
    
    return stats

def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result

def allStats(df):
    df = give_ELO_points(df, 'FTHG','FTAG')
    df = give_points(df, 'FTHG', 'FTAG')
    
    hTeam = df.iloc[0]['HomeTeam']
    aTeam = df.iloc[0]['AwayTeam']
    date = df.iloc[0]['Date']
    stats = matchStats(hTeam, aTeam, df, date)
    
    for i in range(1, df.shape[0]):
        hTeam = df.iloc[i]['HomeTeam']
        aTeam = df.iloc[i]['AwayTeam']
        date = df.iloc[i]['Date']
        stats = stats.append(matchStats(hTeam, aTeam, df, date))

    #Filling NaNs with mean of columns
    stats = stats.apply(lambda x: x.fillna(x.mean()), axis=0)

    #Adding results of matches
    stats['FTHG'] = df['FTHG'].values
    stats['FTAG'] = df['FTAG'].values
    
    return stats
        
def to_date(df, column_name):
    
    df2 = df.copy()
    df2['Date'] = pd.to_datetime(df2['Date'])
    for i in range(df.shape[0]):
        if(df2.iloc[i,2].day < 13):
            df.iloc[i,2] = datetime.datetime.strptime(df.iloc[i,2], '%Y-%d-%m')
        else:
            df.iloc[i,2] = datetime.datetime.strptime(df.iloc[i,2], '%Y-%m-%d')
    
    return df