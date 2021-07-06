# Predicting football results with machine learning

This project was made in order to predict football matches based on team form from last 3 matches, last year results and ELO ranking.

## Code
- File _stats.py_ was made to prepare statistics from last few seasons on which ML model can learn.
- File _main.py_ contains ML models, their comparison and prediction of last games of current season. This program predict result, then save it, and basing on saved results and previous results predicts next match.
- File _results.py_ compares real and predicted results and visualize them on plots.
- File _functions.py_ containts used functions.
- File _matchesInfo.py_ download and save football data to data folder.

## Results
Real top6

![plot_real_top6](https://user-images.githubusercontent.com/77171262/117691507-41276180-b1bc-11eb-9f1b-672af7581efd.png)

My prediction

![plot_pred_top6](https://user-images.githubusercontent.com/77171262/117691394-23f29300-b1bc-11eb-8ed8-d5bfd50e22fa.png)

Real bottom 5

![plot_real_bt5](https://user-images.githubusercontent.com/77171262/117694516-88632180-b1bf-11eb-8865-b2d7f0505525.png)

My prediction

![plot_pred_bt5](https://user-images.githubusercontent.com/77171262/117694596-9ca71e80-b1bf-11eb-8e17-8cc4e4751754.png)


## Versions
- All used packages and them versions are listed in  _requirements.txt_  file
- Python 3.8
- Anaconda 2020.07
