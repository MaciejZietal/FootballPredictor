import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from functions import make_table, generateStats, normalize, give_points

#Loading stats
stats = pd.read_csv('data/stats.csv')
#Filling na's
nans = stats.columns[stats.isna().any()].tolist()
stats[nans] = stats[nans].fillna(value=stats[nans].mean())

#Spliting into x and y
X = stats.iloc[:,:-5]
y = stats.iloc[:,[-2,-1]]

#Normalizating data
normalizedX = normalize(X)

#Splitting data to train and test
X_train, X_test, y_train, y_test = train_test_split(normalizedX, y)

################################  Models  #####################################
#Linear Regression
print("Linear Regression")
#Home teams
lrH = LinearRegression()
lrH.fit(X_train, y_train.iloc[:,0])
lryH_pred = lrH.predict(X_test)
for i in range(len(lryH_pred)):
    lryH_pred[i] = round(lryH_pred[i])
print((lryH_pred==y_test.iloc[:,0]).mean())

#Away Teams
lrA = LinearRegression()
lrA.fit(X_train, y_train.iloc[:,1])
yA_pred = lrA.predict(X_test)
for i in range(len(yA_pred)):
    yA_pred[i] = round(yA_pred[i])
print((yA_pred==y_test.iloc[:,1]).mean())


#Polynomial Regression
print("Polynomial Regression")
poly_reg = PolynomialFeatures(degree=2)
X_poly = poly_reg.fit_transform(X_train)

#Home teams
pol_regH = LinearRegression()
pol_regH.fit(X_poly, y_train.iloc[:,0])
plH_pred = pol_regH.predict(poly_reg.fit_transform(X_test))
for i in range(len(plH_pred)):
    plH_pred[i] = round(plH_pred[i])
print((plH_pred==y_test.iloc[:,0]).mean())

#Away teams
pol_regA = LinearRegression()
pol_regA.fit(X_poly, y_train.iloc[:,1])
plA_pred = pol_regA.predict(poly_reg.fit_transform(X_test))
for i in range(len(plA_pred)):
    plA_pred[i] = round(plA_pred[i])
print((plA_pred==y_test.iloc[:,1]).mean())


#Decission tree
print("Decision tree")
#Home teams
dtH = DecisionTreeRegressor()
dtH.fit(X_train,y_train.iloc[:,0])
dtH_pred = dtH.predict(X_test)
print((dtH_pred==y_test.iloc[:,0]).mean())

#Away teams
dtA = DecisionTreeRegressor()
dtA.fit(X_train,y_train.iloc[:,1])
dtA_pred = dtA.predict(X_test)
print((dtA_pred==y_test.iloc[:,1]).mean())


#Random forest
print("Random forest")
#Home teams
rfH = RandomForestRegressor()
rfH.fit(X_train,y_train.iloc[:,0])
rfH_pred = rfH.predict(X_test)
for i in range(len(rfH_pred)):
    rfH_pred[i] = round(rfH_pred[i])
print((rfH_pred==y_test.iloc[:,0]).mean())

#Away teams
rfA = RandomForestRegressor()
rfA.fit(X_train,y_train.iloc[:,1])
rfA_pred = rfA.predict(X_test)
for i in range(len(rfA_pred)):
    rfA_pred[i] = round(rfA_pred[i])
print((rfA_pred==y_test.iloc[:,1]).mean())

##############################################################################

#Testing models
real_res = give_points(y_test,'HGoals','AGoals')
lr_res = give_points(pd.DataFrame({'HGoals':lryH_pred,'AGoals':yA_pred}),'HGoals','AGoals')
pl_res = give_points(pd.DataFrame({'HGoals':plH_pred,'AGoals':plA_pred}),'HGoals','AGoals')
dt_res = give_points(pd.DataFrame({'HGoals':dtH_pred,'AGoals':dtA_pred}),'HGoals','AGoals')
rf_res = give_points(pd.DataFrame({'HGoals':rfH_pred,'AGoals':rfA_pred}),'HGoals','AGoals')

print((real_res.reset_index(drop=True)['HPts']==lr_res.reset_index(drop=True)['HPts']).mean())
print((real_res.reset_index(drop=True)['HPts']==pl_res.reset_index(drop=True)['HPts']).mean())
print((real_res.reset_index(drop=True)['HPts']==dt_res.reset_index(drop=True)['HPts']).mean())
print((real_res.reset_index(drop=True)['HPts']==rf_res.reset_index(drop=True)['HPts']).mean())
#The best model is LR

d20_21 = pd.read_csv('data/d20_21.csv')
d20_21 = d20_21.iloc[:,:8]
d19_20 = pd.read_csv('data/d19_20.csv')
d18_19 = pd.read_csv('data/d18_19.csv')
d17_18 = pd.read_csv('data/d17_18.csv')
stats2 = pd.concat([d17_18,d18_19,d19_20,d20_21.iloc[:-120]])
stats2 = stats2.iloc[:,:8]
stats2['Date'] = pd.to_datetime(stats2['Date'])
d20_21['Date'] = pd.to_datetime(d20_21['Date'])


#Predicting 
for i in range(d20_21.iloc[-120:].shape[0]):
    hTeam = d20_21.iloc[i-120]['HomeTeam']
    aTeam = d20_21.iloc[i-120]['AwayTeam']
    date = d20_21.iloc[i-120]['Date']
    
    #Generating stats for match
    stat = generateStats(stats2, hTeam, aTeam, date)
    print(stat.isna().sum())
    #Replacing NAN with mean from stat df
    col_means = stats.mean()
    stat = stat.fillna(col_means)
    
    #Adding row with stats to stats df
    X = X.append(stat, ignore_index=True)
    
    normalizedX = normalize(X)
    print(stat)
    #Predicting goals
    Hprediction = lrH.predict(normalizedX.iloc[-1].values.reshape(1,16))[0]
    Aprediction = lrA.predict(normalizedX.iloc[-1].values.reshape(1,16))[0]
    Hprediction = round(Hprediction)
    Aprediction = round(Aprediction)
    if(Hprediction > Aprediction):
        hpts = 3
        apts = 0
        ehpts = 1
        eapts = 0
    elif(Hprediction < Aprediction):
        hpts = 0
        apts = 3
        ehpts = 0
        eapts = 1
    else:
        hpts = 1
        apts = 1
        ehpts = 0.5
        eapts = 0.5
    
    row = pd.DataFrame({'Unnamed: 0':[stats2.iloc[-1]['Unnamed: 0']+1],
                        'Div':['E0'],'Date':[date],'Time':[0],'HomeTeam':[hTeam],
                        'AwayTeam':[aTeam],'FTHG':[Hprediction],
                        'FTAG':[Aprediction],'HPTS':[hpts],
                        'APTS':[apts],'ELOHPTS':[ehpts],'ELOAPTS':[eapts]})
    stats2 = stats2.append(row)
   
stats2.iloc[-120:].to_csv("data/pred_res.csv", index=False)
    
