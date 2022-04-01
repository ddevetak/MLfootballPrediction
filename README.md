# MLfootballPrediction
Machine learning prediction of football matches

Using scrapy and sklearn packages for data extraction and machine learning prediction of football matches.

## Tutorial

1. Install scrapy  `pip install scrapy`
  
2. Install scikit-learn  `pip install sklearn`

3. Download code `git clone https://github.com/ddevetak/MLfootballPrediction.git`

4. Get next matches `./getMatches.sh premier` (england premier league)


`pd.read_csv("01-04-2022/premier/games.csv")`

`
homeTeam         awayTeam   league                       odds        date   time
0        Liverpool          Watford  premier  ['1.13', '9.28', '20.98']  2022-04-02  13:30
1         Brighton          Norwich  premier   ['1.50', '4.09', '7.39']  2022-04-02  16:00
2          Burnley  Manchester City  premier  ['13.72', '6.51', '1.22']  2022-04-02  16:00
3          Chelsea        Brentford  premier   ['1.35', '4.96', '9.90']  2022-04-02  16:00
4            Leeds      Southampton  premier   ['2.41', '3.58', '2.85']  2022-04-02  16:00
5           Wolves      Aston Villa  premier   ['3.00', '3.08', '2.57']  2022-04-02  16:00
6   Manchester Utd        Leicester  premier   ['1.51', '4.55', '6.05']  2022-04-02  18:30
7         West Ham          Everton  premier   ['1.78', '3.74', '4.59']  2022-04-03  15:00
8        Tottenham        Newcastle  premier   ['1.51', '4.35', '6.54']  2022-04-03  17:30
9   Crystal Palace          Arsenal  premier   ['4.04', '3.38', '1.98']  2022-04-04  21:00
10         Burnley          Everton  premier   ['2.65', '3.19', '2.75']  2022-04-06  20:30
`


