import numpy as np
import scrapy
#from scrapy_splash import SplashRequest
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

        URLS = {
 
        # england
        'premier':  ['https://www.betexplorer.com/soccer/england/premier-league/'] ,   
        'cha':      ['https://www.betexplorer.com/soccer/england/championship/'] ,   
        'eng1':     ['https://www.betexplorer.com/soccer/england/league-one/' ],
        'eng2':     ['https://www.betexplorer.com/soccer/england/league-two/' ],
        'national': ['https://www.betexplorer.com/soccer/england/national-league/'],
        'north':    ['https://www.betexplorer.com/soccer/england/national-league-north/'],
        'south':    ['https://www.betexplorer.com/soccer/england/national-league-south/']

        }


        urls = URLS[self.parameter1] 

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        leagueNames = {
                        "Premier League":      "premier",
                        "Championship":        "cha",
                        "League One":          "eng1",
                        "League Two":          "eng2",
                        "National League":     "national"
                      }
         
        item = nextMatches()

        #                                                wrap-section__header__title
        currentLeagueName = response.xpath('//h1[@class="wrap-section__header__title"]/text()').extract()[0].split(' 20')[0]
        currentLeagueName = leagueNames[currentLeagueName]

        teamNames, results, dateTime, odds = [], [], [], []

        # can have COMB. POST., no odds... 
        for ss in response.xpath('//table[@class="table-main table-main--leaguefixtures h-mb15"]/tr')[1:]:
            
            x1 = ss.xpath("./td/a/span/strong/text() | ./td/a/span/text()").extract()  # team names
            checkIfOdss = ss.xpath("./td/@data-oid").extract()                         # check if empty odds
            x2 = ss.xpath("./td/button/@data-odd").extract()                           # ODDS
            x3 = ss.xpath("./td/text() | ./td/strong/span/text()").extract()[-1]       # date

            if '' in checkIfOdss or x3 == 'POSTP.': continue        
            teamNames.append(x1 + [currentLeagueName])
            odds.append(x2)
            dateTime.append(x3)

        if dateTime:
          fullData = getDataTime(teamNames, odds, dateTime)

        item['seasonData'] = fullData
        return item

