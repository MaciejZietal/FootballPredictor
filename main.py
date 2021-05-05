import pandas as pd
import numpy as np
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from functions import make_table, generateStats

#Loading stats
stats = pd.read_csv('data/stats.csv')
#Filling na's
nans = stats.columns[stats.isna().any()].tolist()
stats[nans] = stats[nans].fillna(value=stats[nans].mean())

#Spliting into x and y
X = stats.iloc[:,:-5]
y = stats.iloc[:,[-2,-1]]

#Normalizating data
scaler = Normalizer().fit(X)
normalizedX = scaler.transform(X)

#Splitting data to train and test
X_train, X_test, y_train, y_test = train_test_split(normalizedX, y)

#Linear Regression for home teams
lrH = DecisionTreeRegressor()
lrH.fit(X_train, y_train.iloc[:,0])
yH_pred = lrH.predict(X_test)
for i in range(len(yH_pred)):
    yH_pred[i] = round(yH_pred[i])
print((yH_pred==y_test.iloc[:,0]).mean())

#Linear regression for away teams
lrA = DecisionTreeRegressor()
lrA.fit(X_train, y_train.iloc[:,1])

yA_pred = lrA.predict(X_test)
for i in range(len(yA_pred)):
    yA_pred[i] = round(yA_pred[i])
print((yA_pred==y_test.iloc[:,1]).mean())

d20_21 = pd.read_csv('data/d20_21.csv')
d20_21 = d20_21.iloc[:,:8]
d20_21['HPred'] = np.empty(d20_21.shape[0])
d20_21['APred'] = np.empty(d20_21.shape[0])
d19_20 = pd.read_csv('data/d19_20.csv')
d18_19 = pd.read_csv('data/d18_19.csv')
d17_18 = pd.read_csv('data/d17_18.csv')
stats2 = pd.concat([d19_20,d18_19,d17_18])
stats2 = stats2.iloc[:,:8]
stats2['Date'] = pd.to_datetime(stats2['Date'])
d20_21['Date'] = pd.to_datetime(d20_21['Date'])

hpts=[]
apts=[]
ehpts=[]
eapts=[]
for i in range(stats2.shape[0]):
    if stats2.iloc[i]['FTHG'] > stats2.iloc[i]['FTAG']:
        hpts.append(3)
        apts.append(1)
        ehpts.append(1)
        eapts.append(0)
    elif stats2.iloc[i]['FTHG'] < stats2.iloc[i]['FTAG']:
        hpts.append(0)
        apts.append(3)
        ehpts.append(0)
        eapts.append(1)
    else:   
        hpts.append(1)
        apts.append(1)
        ehpts.append(0.5)
        eapts.append(0.5)
stats2['HPTS'] = hpts
stats2['APTS'] = apts
stats2['ELOHPTS'] = ehpts
stats2['ELOAPTS'] = eapts

for i in range(d20_21.shape[0]):
    hTeam = d20_21.iloc[i]['HomeTeam']
    aTeam = d20_21.iloc[i]['AwayTeam']
    date = d20_21.iloc[i]['Date']
    
    #Generating stats for match
    stat = generateStats(stats2, hTeam, aTeam, date)
    #Predicting goals
    Hprediction = lrH.predict(stat)[0]
    Aprediction = lrA.predict(stat)[0]
    
    #d20_21.iloc[i]['FTHG'] = Hprediction
    #d20_21.iloc[i]['FTAG'] = Aprediction
    if(Hprediction > Aprediction):
        hpts = 3
        apts = 0
        ehpts = 1
        eapts = 0
    elif(Hprediction < Aprediction):
        hpts = 0
        apts = 3
        ehpts=0
        eapts=1
    else:
        hpts = 1
        apts = 1
        ehpts=0.5
        eapts=0.5
    
    row = pd.DataFrame({'Unnamed: 0':[stats2.iloc[-1]['Unnamed: 0']+1],
                        'Div':['E0'],'Date':[date],'Time':[0],'HomeTeam':[hTeam],
                        'AwayTeam':[aTeam],'FTHG':[Hprediction],
                        'FTAG':[Aprediction],'HPTS':[hpts],
                        'APTS':[apts],'ELOHPTS':[ehpts],'ELOAPTS':[eapts]})
    stats2 = stats2.append(row)