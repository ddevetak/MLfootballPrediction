# MLfootballPrediction
Machine learning prediction of football matches

Using scrapy and sklearn packages for data extraction and machine learning prediction of football matches.

## Tutorial

1. Install scrapy  `pip install scrapy`
  
2. Install scikit-learn  `pip install sklearn`

3. Download code `git clone https://github.com/ddevetak/MLfootballPrediction.git`

4. Get next matches `./getMatches.sh premier` (england premier league)


`pd.read_csv("01-04-2022/premier/games.csv")`

<img src="https://github.com/ddevetak/MLfootballPrediction/blob/main/figures/games.png" width="660" height="200">


5. Get previous historical games `./previousMatches.sh premier`

`pd.read_csv("01-04-2022/premier/finalData.csv")`

<img src="https://github.com/ddevetak/MLfootballPrediction/blob/main/figures/data.png" width="600" height="200">


6. Predict outcomes `run predict.py 01-04-2022/premier/`.   
For model **LogisticRegression** is used. Other models are possible. Outcome = 1 (home win), 0 (draw), -1 (away win) 


<img src="https://github.com/ddevetak/MLfootballPrediction/blob/main/figures/predictions.png" width="720" height="230">



