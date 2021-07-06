import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from functions import give_points, normalize

#Importing data
stats = pd.read_csv('data/stats.csv')

#Test and train values
x = stats.iloc[:,1:-2]
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

for i in range(len(lrH_pred)):
    lrH_pred[i] = round(lrH_pred[i])
    
#Away
lrA = LinearRegression()
lrA.fit(xA_train, yA_train)
lrA_pred = lrA.predict(xA_test)

for i in range(len(lrA_pred)):
    lrA_pred[i] = round(lrA_pred[i])
    
#Polynomial LR
polynomial_features = PolynomialFeatures(degree=2)

#Home
pLRH = LinearRegression()
pLRH_model = Pipeline(steps=[('PL feature', polynomial_features),('regressor',pLRH)])
pLRH_model.fit(xH_train, yH_train)
pLRH_pred = pLRH_model.predict(xH_test)

for i in range(len(pLRH_pred)):
    pLRH_pred[i] = round(pLRH_pred[i])
    if(pLRH_pred[i]<0):
        pLRH_pred[i]=0
    
#Away
pLRA = LinearRegression()
pLRA_model = Pipeline(steps=[('PL feature', polynomial_features),('regressor',pLRA)])
pLRA_model.fit(xA_train, yA_train)
pLRA_pred = pLRA_model.predict(xA_test)

for i in range(len(pLRA_pred)):
    pLRA_pred[i] = round(pLRA_pred[i])
    if(pLRA_pred[i]<0):
        pLRA_pred[i]=0
        
#Decision Tree
#Home
dtrH = DecisionTreeRegressor()
dtrH.fit(xH_train, yH_train)
dtrH_pred = dtrH.predict(xH_test)

#Away
dtrA = DecisionTreeRegressor()
dtrA.fit(xA_train, yA_train)
dtrA_pred = dtrA.predict(xA_test)

#Random Forest
#Home
rfH = RandomForestRegressor()
rfH.fit(xH_train, yH_train)
rfH_pred = rfH.predict(xH_test)

for i in range(len(rfH_pred)):
    rfH_pred[i] = round(rfH_pred[i])
    if(rfH_pred[i]<0):
        rfH_pred[i]=0

#Away
rfA = RandomForestRegressor()
rfA.fit(xA_train, yA_train)
rfA_pred = rfA.predict(xA_test)

for i in range(len(rfA_pred)):
    rfA_pred[i] = round(rfA_pred[i])
    if(rfA_pred[i]<0):
        rfA_pred[i]=0
        
#Accuracy of goals prediction
HgoalsAcc = {'LR':(lrH_pred==yH_test).mean(),'PLR':(pLRH_pred==yH_test).mean(),
            'DT':(dtrH_pred==yH_test).mean(),'RF':(rfH_pred==yH_test).mean()}
AgoalsACC = {'LR':(lrA_pred==yA_test).mean(),'PLR':(pLRA_pred==yA_test).mean(),
            'DT':(dtrA_pred==yA_test).mean(),'RF':(rfA_pred==yA_test).mean()}

plt.bar(HgoalsAcc.keys(), HgoalsAcc.values())
plt.title('Accuracy of home goals prediction')
plt.xlabel('ML Algorithm')
plt.ylabel('Accuracy')
plt.show()

plt.bar(AgoalsACC.keys(), AgoalsACC.values())
plt.title('Accuracy of away goals prediction')
plt.xlabel('ML Algorithm')
plt.ylabel('Accuracy')
plt.show()

#Accurancy of points prediction
lr = pd.DataFrame({'hg':lrH_pred,'ag':lrA_pred})
plr = pd.DataFrame({'hg':pLRH_pred,'ag':pLRA_pred})
dtr = pd.DataFrame({'hg':dtrH_pred,'ag':dtrA_pred})
rf = pd.DataFrame({'hg':rfH_pred,'ag':rfA_pred})
y_test = pd.DataFrame({'hg':yH_test.values,'ag':yA_test.values})

lr = give_points(lr, 'hg', 'ag')
plr = give_points(plr, 'hg', 'ag')
dtr = give_points(dtr, 'hg', 'ag')
rf = give_points(rf, 'hg', 'ag')
y_test = give_points(y_test, 'hg', 'ag')

ptsACC = {'LR':(lr['HPts']==y_test['HPts']).mean(),'PLR':(plr['HPts']==y_test['HPts']).mean(),
          'DT':(dtr['HPts']==y_test['HPts']).mean(),'RF':(rf['HPts']==y_test['HPts']).mean()}

plt.bar(ptsACC.keys(), ptsACC.values())
plt.title('Accuracy of result (win/draw/loss) prediction')
plt.xlabel('ML Algorithm')
plt.ylabel('Accuracy')
plt.show()