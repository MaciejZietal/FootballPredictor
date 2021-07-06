import pandas as pd
from functions import allStats, to_date

#Reading data
d1920 = pd.read_csv('data/d19_20.csv')
d1819 = pd.read_csv('data/d18_19.csv')
d1718 = pd.read_csv('data/d17_18.csv')
d1617 = pd.read_csv('data/d16_17.csv')
d1516 = pd.read_csv('data/d15_16.csv')

data = pd.concat([d1920,d1819,d1718,d1617,d1516])
data = to_date(data, 'Date')

#Generating stats
stats = allStats(data)

#Saving stats
stats.to_csv('data/stats.csv')