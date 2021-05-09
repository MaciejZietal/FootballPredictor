import matplotlib.pyplot as plt
import pandas as pd
from functions import make_table
d20_21 = pd.read_csv("data/d20_21.csv")
pred_res = pd.read_csv("data/pred_res.csv")

#Table of the first twenty rounds
table20 = make_table(d20_21.iloc[:200],'FTHG','FTAG','HomeTeam','AwayTeam')
#Real table of last rounds
real_table = make_table(d20_21.iloc[200:],'FTHG','FTAG','HomeTeam','AwayTeam')
#Predicted table of last rounds
pred_table = make_table(pred_res,'FTHG','FTAG','HomeTeam','AwayTeam')

top6 = ['Chelsea','Leicester','Man United','Liverpool','Man City','West Ham']

table20_top6 = {key: table20[key] for key in top6}
pred_table_top6 = {key: pred_table[key] for key in top6}
real_table_top6 = {key: real_table[key] for key in top6}

fig,ax=plt.subplots()
ax.bar(table20_top6.keys(),table20_top6.values(),color="lightblue",label="First 20 games")
ax.bar(real_table_top6.keys(),real_table_top6.values(), bottom=[table20_top6[i] for i in table20_top6.keys()],color="darkblue",label="Real last 12 games")
plt.legend()
plt.show()

fig1,ax1=plt.subplots()
ax1.bar(table20_top6.keys(),table20_top6.values(),color="lightblue",label="First 20 games")
ax1.bar(pred_table_top6.keys(),pred_table_top6.values(), bottom=[table20_top6[i] for i in table20_top6.keys()],color="darkblue",label="Predicted last 12 games")
plt.legend()
plt.show()

