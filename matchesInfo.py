import pandas as pd

#Downloading football data
d20_21 = pd.read_csv("https://www.football-data.co.uk/mmz4281/2021/E0.csv", parse_dates=['Date'])
d19_20 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1920/E0.csv", parse_dates=['Date'])
d18_19 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1819/E0.csv", parse_dates=['Date'])
d17_18 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1718/E0.csv", parse_dates=['Date'])
d16_17 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1617/E0.csv", parse_dates=['Date'])
d15_16 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1516/E0.csv", parse_dates=['Date'])
d14_15 = pd.read_csv("https://www.football-data.co.uk/mmz4281/1415/E0.csv", parse_dates=['Date'])

#saving files
d20_21.to_csv('data/d20_21.csv')
d19_20.to_csv('data/d19_20.csv')
d18_19.to_csv('data/d18_19.csv')
d17_18.to_csv('data/d17_18.csv')
d16_17.to_csv('data/d16_17.csv')
d15_16.to_csv('data/d15_16.csv')
d14_15.to_csv('data/d14_15.csv')