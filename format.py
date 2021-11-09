import pandas as pd
import numpy as np
import ast
import math
import matplotlib.pyplot as plt
# sklearn regressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeRegressor

from sklearn.model_selection import train_test_split

df = pd.read_csv("finalData.csv", index_col=False)

teamList = list(set(df['homeTeam']))

gamesPerTeam = dict()

for teamName in teamList:
   games = df.loc[(df['homeTeam'] == teamName) | (df['awayTeam'] == teamName)]
   gamesPerTeam[teamName] = games

blockSize = 6 # how many previous matches to take for input definition

inputFrame =  pd.DataFrame()
inputFrame2 = pd.DataFrame()

Count = -1

# collect all matches for which N previous data points (games) exist
for index, row in df.iterrows():

    homeTeam, awayTeam, matchDate = row['homeTeam'], row['awayTeam'], row['date']
    odds = [ float(x) for x in ast.literal_eval(row['odds']) ]
    oddsRatio = odds[0]/odds[2]

    avHomeTeamGoalsScored, avHomeTeamGoalsConceded = [], []
    avAwayTeamGoalsScored, avAwayTeamGoalsConceded = [], []

    gamesHome = gamesPerTeam[homeTeam]
    gamesAway = gamesPerTeam[awayTeam]

    homeBlock = gamesHome[gamesHome['date'] < matchDate]  # for given home team get matches before defined 'date'
    awayBlock = gamesAway[gamesAway['date'] < matchDate]

    # add to result ':h' or ':a' label to differentiate home, away case
    for hindex, hrow in homeBlock.iterrows():
        cResult = homeBlock.loc[hindex, 'result']
        if homeTeam == hrow['homeTeam']: homeBlock.loc[hindex]['result'] = cResult + ':h'
        if homeTeam == hrow['awayTeam']: homeBlock.loc[hindex]['result'] = cResult + ':a'

    for hindex, hrow in awayBlock.iterrows():
        cResult = awayBlock.loc[hindex, 'result']
        if awayTeam == hrow['homeTeam']: awayBlock.loc[hindex]['result'] = cResult + ':h'
        if awayTeam == hrow['awayTeam']: awayBlock.loc[hindex]['result'] = cResult + ':a'

    if len(homeBlock) >= blockSize and len(awayBlock) >= blockSize:

        Count += 1

        resHome = list(homeBlock['result'])[0:blockSize][::-1]  # last "blockSize" matches for given home team
        resAway = list(awayBlock['result'])[0:blockSize][::-1]

        resHome2 = [x.split(":") for x in resHome]
        resAway2 = [x.split(":") for x in resAway]

        for xx in resHome2:
            if xx[2] == 'h': 
                avHomeTeamGoalsScored.append(int(xx[0]))
                avHomeTeamGoalsConceded.append(int(xx[1]))
            if xx[2] == 'a': 
                avHomeTeamGoalsScored.append(int(xx[1]))
                avHomeTeamGoalsConceded.append(int(xx[0]))

        for xx in resAway2:
            if xx[2] == 'h': 
                avAwayTeamGoalsScored.append(int(xx[0]))
                avAwayTeamGoalsConceded.append(int(xx[1]))
            if xx[2] == 'a': 
                avAwayTeamGoalsScored.append(int(xx[1]))
                avAwayTeamGoalsConceded.append(int(xx[0]))


        Result = int(row['result'][0]) - int(row['result'][2])
        Wodds = None
        if   Result > 0: Wodds = odds[0] 
        elif Result < 0: Wodds = odds[2] 
        else: Wodds = odds[1] 

        inputData = {"homeTeam": homeTeam, "awayTeam": awayTeam, \
                     "avHomeTeamScored": sum(avHomeTeamGoalsScored)/len(resHome2), \
                     "avHomeTeamConceded": sum(avHomeTeamGoalsConceded)/len(resHome2), \

                     "avAwayTeamScored": sum(avAwayTeamGoalsScored)/len(resHome2), \
                     "avAwayTeamConceded": sum(avAwayTeamGoalsConceded)/len(resHome2), \

                     "oddsRatio": oddsRatio, "Wodds": Wodds, "result": np.sign(Result) }

        inputData2 = {"homeTeam": homeTeam, "awayTeam": awayTeam, \
                     "homeData": str(resHome), "awayData": str(resAway), \
                     "oddsRatio": oddsRatio, "Wodds": Wodds, "result": Result }



        inputFrame =  inputFrame.append(pd.DataFrame(inputData,  index=[Count]))
        inputFrame2 = inputFrame2.append(pd.DataFrame(inputData2, index=[Count]))

        #if index == 0: break
   

###########################################
# model data


X = inputFrame[["avHomeTeamScored", "avHomeTeamConceded", "avAwayTeamScored", "avAwayTeamConceded", "oddsRatio", "Wodds"]].to_numpy()
y = inputFrame["result"].to_numpy()

#model = GradientBoostingRegressor()
model = GradientBoostingClassifier()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

model.fit(X_train[:, 0:5], y_train)


print( f'train model score = {model.score(X_train[:, 0:5], y_train):.3f}' )
print( f'test model score  = {model.score(X_test[:, 0:5], y_test):.3f}' )
print( f'test model prob   = {1/model.score(X_test[:, 0:5], y_test):.3f}' )
print( f'mean test odds    = {np.mean(X_test[:, 5]):.3f}' )










