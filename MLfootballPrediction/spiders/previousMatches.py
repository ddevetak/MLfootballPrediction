import numpy as np
import scrapy
from scrapy_splash import SplashRequest
from MLfootballPrediction.items import MlfootballpredictionItem
import pandas as pd
from datetime import datetime, timedelta

class getMatchesSpider(scrapy.Spider):
    name = "previousMatches"

    def start_requests(self):

        URLS = {
                "premier":[

                      'https://www.betexplorer.com/soccer/england/premier-league/results',
                      'https://www.betexplorer.com/soccer/england/premier-league-2020-2021/results/',
                      'https://www.betexplorer.com/soccer/england/premier-league-2019-2020/results/',
                      'https://www.betexplorer.com/soccer/england/premier-league-2018-2019/results/',
                      'https://www.betexplorer.com/soccer/england/premier-league-2017-2018/results/',
                      'https://www.betexplorer.com/soccer/england/premier-league-2016-2017/results/',
                      'https://www.betexplorer.com/soccer/england/premier-league-2015-2016/results/',
                      'https://www.betexplorer.com/soccer/england/premier-league-2014-2015/results/'
                ]
                }

        urls = URLS[self.parameter1] 


        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        item = MlfootballpredictionItem()

        # NEW format
        teamNames, results, dates, odds = [], [], [], []

        currentLeagueName = response.xpath('//h1[@class="wrap-section__header__title"]/span/text()').extract()[1]

        print(currentLeagueName)

        for ss in response.xpath('//div[@id="js-leagueresults-all"]/div/div/table/tr')[1:]:

           if 'POSTP.' in ss.xpath("./td/a/span/text()").extract(): continue 

           x1 = ss.xpath("./td/a/span/strong/text() | ./td/a/span/text()").extract()  # teamNames
           x2 = ss.xpath("./td/a/text() | ./td/a/span/@title").extract()              # result 
           x3 = ss.xpath("./td/@data-odd | ./td/span/span/span/@data-odd").extract()  # ODDS
           x4 = ss.xpath("./td/text()").extract()                                     # date  


           if not x2: continue  # reading if not filled
           if x2[1] == 'Canceled': continue
           results.append(x2[1])
           if x1:                    teamNames.append(x1)
           if x1 and x3:             odds.append(x3)
           if x1 and len(x3) == 0:   odds.append([3.33, 3.33, 3.33])
           if x4:                    dates.append(x4[-1])


        year =  datetime.today().strftime('%Y')
        yesterday0 = datetime.now() - timedelta(1)
        yesterday = str(yesterday0.day) + "." + str(yesterday0.month) + "." + str(yesterday0.year)

        for cDate in dates:
            if len(cDate)==6:  # 6 = len('02.11.')
              dates[dates.index(cDate)] = cDate + year
            if cDate == "Yesterday":  
              dates[dates.index(cDate)] = yesterday


        DATA = list(zip(teamNames, results, odds, dates))

        fullData = []
        for xx in DATA:
          tempDict = {"homeTeam": xx[0][0], "awayTeam": xx[0][1], "league": currentLeagueName, "result":xx[1], "odds": list(xx[2]), "date": pd.to_datetime(xx[3], format='%d.%m.%Y')} # final Y-M-D
          fullData.append(tempDict)

        item["seasonData"] = fullData  

        return item
 
