import pandas as pd
import numpy as np
import ast
import math
#from tabulate import tabulate
import sys
import pickle

# sklearn regressor
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score

from sklearn import model_selection

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV



 
def singleFormating(df, gamesPerTeam, blockSize, dataType):  # df is full data - but here for match looping

    inputFrame =   pd.DataFrame()
    inputFrame2 =  pd.DataFrame()

    Count = -1
    
    for index, row in df.iterrows():
    
        homeTeam, awayTeam, matchDate = row['homeTeam'], row['awayTeam'], row['date']
        odds = [ float(x) for x in ast.literal_eval(row['odds']) ]
        oddsRatio = odds[0]/odds[2]
    
        avHomeTeamGoalsScored, avHomeTeamGoalsConceded = [], []
        avAwayTeamGoalsScored, avAwayTeamGoalsConceded = [], []

        hW, hD, hL = 0, 0, 0
        aW, aD, aL = 0, 0, 0
    
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
    
            resHome2 = np.array([x.split(":") for x in resHome])
            resAway2 = np.array([x.split(":") for x in resAway])

            resHome2h, resHome2a  = resHome2[resHome2[:, 2] == 'h'], resHome2[resHome2[:, 2] == 'a']
            resAway2h, resAway2a  = resAway2[resAway2[:, 2] == 'h'], resAway2[resAway2[:, 2] == 'a']

            for ii in resHome2h:
                if int(ii[0]) - int(ii[1])   > 0: hW += 1
                elif int(ii[0]) - int(ii[1]) < 0: hL += 1
                else: hD += 1          
            for ii in resHome2a:
                if int(ii[1]) - int(ii[0])   > 0: hW += 1
                elif int(ii[1]) - int(ii[0]) < 0: hL += 1
                else: hD += 1          

            for ii in resAway2h:
                if int(ii[0]) - int(ii[1])   > 0: aW += 1
                elif int(ii[0]) - int(ii[1]) < 0: aL += 1
                else: aD += 1          
            for ii in resAway2a:
                if int(ii[1]) - int(ii[0])   > 0: aW += 1
                elif int(ii[1]) - int(ii[0]) < 0: aL += 1
                else: aD += 1          

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
    
            if dataType == 'historical': 
               tempRes = row['result'].split(":")
               Result = int(tempRes[0]) - int(tempRes[1])
               Wodds = None
               if   Result > 0: Wodds = odds[0] 
               elif Result < 0: Wodds = odds[2] 
               else: Wodds = odds[1] 
            else:
               Result =11
               Wodds = None 
       
            inputData = {"homeTeam": homeTeam, "awayTeam": awayTeam, \
                         "avHomeTeamScored": sum(avHomeTeamGoalsScored), \
                         "avHomeTeamConceded": sum(avHomeTeamGoalsConceded), \
                         "avAwayTeamScored": sum(avAwayTeamGoalsScored), \
                         "avAwayTeamConceded": sum(avAwayTeamGoalsConceded), \
                         "hW": hW, "hD": hD, "hL": hL,    
                         "aW": aW, "aD": aD, "aL": aL,    

                         #"oddsRatio": oddsRatio, "result": np.sign(Result) }
                         "Hodds": odds[0], "Dodds": odds[1], "Aodds": odds[2], "result": np.sign(Result) }
    
    
            inputFrame =  inputFrame.append(pd.DataFrame(inputData,  index=[Count]))

    return inputFrame


class FormatData:

      def __init__(self, fileName, nGames):
      
          self.df = pd.read_csv(fileName, index_col=False)
          self.blockSize = nGames
          self.teamNames = list(set(self.df['homeTeam']))
          self.gamesPerTeam = dict()

          self.inputFrame =  pd.DataFrame()
          self.X_numpy, self.y_numpy = None, None
   
          for teamName in self.teamNames:
            games = self.df.loc[(self.df['homeTeam'] == teamName) | (self.df['awayTeam'] == teamName)]
            self.gamesPerTeam[teamName] = games

          self.fullFormating()  

      def fullFormating(self):    

          self.inputFrame = singleFormating(self.df, self.gamesPerTeam, self.blockSize, 'historical')

          #self.X_numpy = self.inputFrame[["avHomeTeamScored", "avHomeTeamConceded", "avAwayTeamScored", "avAwayTeamConceded", "hW", "hD", "hL", "aW", "aD", "aL", "oddsRatio"]].to_numpy()  # 14 columns
          self.X_numpy = self.inputFrame[["avHomeTeamScored", "avHomeTeamConceded", "avAwayTeamScored", "avAwayTeamConceded", "hW", "hD", "hL", "aW", "aD", "aL", "Hodds", "Dodds", "Aodds"]].to_numpy()  # 14 columns
          self.y_numpy = self.inputFrame["result"].to_numpy()

                 
####################################################
# model data

dataObject = FormatData("./01-04-2022/premier/finalData.csv", 7)   # ger2+, italy1+

X, y = dataObject.X_numpy, dataObject.y_numpy

model =  LogisticRegression(solver = 'liblinear', max_iter=700)
#model = RandomForestClassifier()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=43)

odds_test =  X_test[:, 10:]
X_train, X_test = X_train[:, 0:10], X_test[:, 0:10]


model.fit(X_train, y_train)

odds_compare = np.concatenate((y_test[:, None], model.predict(X_test)[:, None], odds_test), axis = 1)

ODDS = []
for xx in odds_compare:
    if xx[0] == xx[1]:
        if xx[1] ==  1:  ODDS.append(xx[2])
        if xx[1] ==  0:  ODDS.append(xx[3])
        if xx[1] == -1:  ODDS.append(xx[4])

ODDS = sum(ODDS)/len(ODDS)


#print( f'train model score = {model.score(X_train, y_train):.3f}' )
print( f'test model score  = {model.score(X_test, y_test):.3f}' )
print("bookie odds = ", round(ODDS, 2))
print( f'model odds   = {1/model.score(X_test, y_test):.2f}' )


####################################################
# new matches

nextDF = pd.read_csv("./01-04-2022/premier/games.csv")

data16 = singleFormating(nextDF, dataObject.gamesPerTeam, dataObject.blockSize, 'next')
data16 = data16.drop(["result"], axis = 1)
data16 = data16.drop(["Hodds", "Dodds", "Aodds"], axis = 1)

predictions = []

for index, row in data16.iterrows():

    temp = row.to_numpy()[2:][None, :]
    pred = model.predict(temp)

    predictions.append(pred.item())



data16["prediction"] = predictions

print(data16)
