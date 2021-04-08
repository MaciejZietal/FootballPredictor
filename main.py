import pandas as pd
import numpy as np
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from functions import make_table

#Loading stats
stats = pd.read_csv('stats.csv')
#Filling na's
nans = stats.columns[stats.isna().any()].tolist()
stats[nans] = stats[nans].fillna(value=stats[nans].mean())
table = make_table(stats, 'HGoals', 'AGoals', 'HomeTeam', 'AwayTeam')

stats = stats[['last3homeShots', 'last3homeShotsAgs',
       'last3homeShotsTarget', 'last3homeShotsTargetAgs', 'last3homeCorners',
       'last3homeCornersAgs','last3awayShotsTarget', 'last3awayShotsTargetAgs',
       'last3awayCorners', 'last3awayCornersAgs', 'homeELO', 'awayELO',
       'HomeTeam', 'AwayTeam', 'Date', 'HGoals', 'AGoals']]

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

fullSeasonH = lrH.predict(normalizedX)
fullSeasonA = lrA.predict(normalizedX)

mypred = pd.DataFrame({'HTeam':stats['HomeTeam'],'ATeam':stats['AwayTeam'],
                       'HG':fullSeasonH,'AG':fullSeasonA})

myTable = make_table(mypred, 'HG','AG','HTeam','ATeam')