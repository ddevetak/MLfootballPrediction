import numpy as np
import scrapy
from scrapy_splash import SplashRequest
from MLfootballPrediction.items import nextMatches
import pandas as pd
from datetime import datetime, timedelta

def getDataTime(teamNames, odds, dateTime):

        dateTime = np.array([x.split(" ") for x in dateTime])
        date, Time = list(dateTime[:,0]), list(dateTime[:,1])

        uDate = [] # redo because of Today or Tomorrow cases

        for xx in date:
            if xx == 'Tomorrow':
                temp = datetime.now() + timedelta(1)
                temp = str(temp.day) + "." + str(temp.month) + "." + str(temp.year)
                uDate.append(temp)
            elif xx == 'Today':
                temp = datetime.now()
                temp = str(temp.day) + "." + str(temp.month) + "." + str(temp.year)
                uDate.append(temp)
            else:
                xx = xx.split(".")
                temp = str(xx[0]) + "." + str(xx[1]) + "." + str(datetime.now().year)
                uDate.append(temp)

        year =  datetime.today().strftime('%Y')
        for cDate in date:
            if len(cDate)==6:
              date[date.index(cDate)] = cDate + year

        DATA = list(zip(teamNames, odds, uDate, Time))

        fullData = []
        for xx in DATA:
            tempDict = {"homeTeam": xx[0][0], "awayTeam": xx[0][1], "league":xx[0][2], "odds": list(xx[1]), "date": pd.to_datetime(xx[2], format='%d.%m.%Y'), "time": xx[3]} # final Y-M-D
            fullData.append(tempDict)

        return fullData    


class getMatchesSpider(scrapy.Spider):
    name = "nextMatches"

    def start_requests(self):

        urls = [

            'https://www.betexplorer.com/soccer/italy/serie-a/',
        ]


        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        item = nextMatches()

        currentLeagueName = response.xpath('//h1[@class="wrap-section__header__title"]/span/text()').extract()[1]

        teamNames, results, dateTime, odds = [], [], [], []

        # can have COMB. POST., no odds... 
        for ss in response.xpath('//table[@class="table-main table-main--leaguefixtures h-mb15"]/tr')[1:]:
            
            x1 = ss.xpath("./td/a/span/strong/text() | ./td/a/span/text()").extract()  # team names
            checkIfOdss = ss.xpath("./td/@data-oid").extract()                         # check if empty odds
            x2 = ss.xpath("./td/a/@data-odd").extract()                                # ODDS
            x3 = ss.xpath("./td/text() | ./td/strong/span/text()").extract()[-1]       # date

            if '' in checkIfOdss or x3 == 'POSTP.': continue        
            teamNames.append(x1 + [currentLeagueName])
            odds.append(x2)
            dateTime.append(x3)

        if dateTime:
          fullData = getDataTime(teamNames, odds, dateTime)

        item['seasonData'] = fullData
        return item

