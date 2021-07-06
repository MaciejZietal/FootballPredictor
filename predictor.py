import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from functions import normalize, matchStats, to_date

#Importing data
stats = pd.read_csv('data/stats.csv')
stats = stats.iloc[:,1:]
#stats = stats.reset_index(drop=True)
d2021 = pd.read_csv('data/d20_21.csv')
d1920 = pd.read_csv('data/d19_20.csv')
d1819 = pd.read_csv('data/d18_19.csv')
d1718 = pd.read_csv('data/d17_18.csv')
data = pd.concat([d1920,d1819,d1718])

data = data.iloc[:,:25]
d2021 = d2021.iloc[:,:25]

d2021 = to_date(d2021, 'Date')
data = to_date(data, 'Date')

#Test and train values
x = stats.iloc[:,:-2]
y1 = stats.iloc[:,-2]
y2 = stats.iloc[:,-1]

x = normalize(x)

#Home results
xH_train, xH_test, yH_train, yH_test = train_test_split(x, y1, test_size=0.2)

#Away results
xA_train, xA_test, yA_train, yA_test = train_test_split(x, y2, test_size=0.2)

#Linear Regression
#Home
lrH = LinearRegression()
lrH.fit(xH_train, yH_train)
lrH_pred = lrH.predict(xH_test)
    
#Away
lrA = LinearRegression()
lrA.fit(xA_train, yA_train)
lrA_pred = lrA.predict(xA_test)

homePrediction = []
awayPrediction = []
    
#PREDICTION
for i in range(d2021.shape[0]):
    print(i)
    hTeam = d2021.iloc[i]['HomeTeam']
    aTeam = d2021.iloc[i]['AwayTeam']
    date = d2021.iloc[i]['Date']
    stat = matchStats(hTeam, aTeam, data, date)
    data = data.append(d2021.iloc[i])
    stat['FTHG'] = d2021.iloc[i]['FTHG']
    stat['FTAG'] = d2021.iloc[i]['FTAG']
    
    col_means = stats.mean()
    if(stat.isna().sum().sum()>0):
        for i in range(stat.shape[1]):
            stat.iloc[0,i] = col_means[i]
            
    stat = stat.to_numpy()
    stats = stats.append(pd.DataFrame(stat.reshape(1,-1), columns=list(stats)), ignore_index=True)
    
    statsN = normalize(stats.iloc[:,:-2])
    
    stat = statsN.iloc[-1].to_numpy().reshape(1,-1)
    
    hPred = lrH.predict(stat)
    hPred = round(hPred.item())
    homePrediction.append(hPred)
    aPred = lrA.predict(stat)
    aPred = round(aPred.item())
    awayPrediction.append(aPred)
    
results = pd.DataFrame({'hPred':homePrediction,'aPred':awayPrediction,
                        'hResult':d2021['FTHG'],'aResults':d2021['FTAG']})

results.to_csv('data/results.csv')