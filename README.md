# MLfootballPrediction
Machine learning prediction of football matches

Using scrapy and sklearn packages for data extraction and machine learning prediction of football matches.

## Tutorial

1. Install scrapy  `pip install scrapy`
  
2. Install scikit-learn  `pip install sklearn`

3. Download code `git clone https://github.com/ddevetak/MLfootballPrediction.git`

4. Get next matches `./getMatches.sh premier` (england premier league)


`pd.read_csv("31-01-2025/premier/games.csv")`

<img src="https://github.com/ddevetak/MLfootballPrediction/blob/main/figures/games.png" width="660" height="200">


5. Get previous historical games `./previousMatches.sh premier`

`pd.read_csv("31-01-2025/premier/finalData.csv")`

<img src="https://github.com/ddevetak/MLfootballPrediction/blob/main/figures/games.png" width="600" height="200">


6. Predict outcomes `python predict.py 31-31-2025/premier/`.   
For model **LogisticRegression** is used. Other models are possible. Outcome = 1 (home win), 0 (draw), -1 (away win) 


<img src="https://github.com/ddevetak/MLfootballPrediction/blob/main/figures/predictions.png" width="720" height="190">



