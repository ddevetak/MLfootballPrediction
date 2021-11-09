import numpy as np
import scrapy
from MLfootballPrediction.items import MlfootballpredictionItem
import pandas as pd
from datetime import datetime, timedelta

class getMatchesSpider(scrapy.Spider):
    name = "nextMatches"

    def start_requests(self):

        urls = [
            'https://www.betexplorer.com/soccer/norway/eliteserien/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        item = MlfootballpredictionItem()

        # matches, results, odds and time 
        matches = np.array(response.xpath('//table[@class="table-main table-main--leaguefixtures h-mb15"]/tr/td/a/span/text() | \
            //table[@class="table-main table-main--leaguefixtures h-mb15"]/tr/td/a/span/text()').extract())
        matches.shape = (int(len(matches)/2), 2)

        # formating date
        dateTime =  response.xpath('//table[@class="table-main table-main--leaguefixtures h-mb15"]/tr/td/text()').extract()
        dateTime = np.array([x.split(" ") for x in dateTime if len(x) > 5])
        date, Time = list(dateTime[:,0]), list(dateTime[:,1])
        
        year =  datetime.today().strftime('%Y')
        yesterday0 = datetime.now() - timedelta(1)
        yesterday = str(yesterday0.day) + "." + str(yesterday0.month) + "." + str(yesterday0.year)
       
        for cDate in date:
            if len(cDate)==6:
              date[date.index(cDate)] = cDate + year


        odds = np.array(response.xpath('//table[@class="table-main table-main--leaguefixtures h-mb15"]/tr/td/a/@data-odd').extract())
        odds.shape = (len(matches), 3)
        
        DATA = list(zip(matches, odds, date, Time))

        fullData = []
        for xx in DATA:
            tempDict = {"homeTeam": xx[0][0], "awayTeam": xx[0][1], "odds": list(xx[1]), "date": pd.to_datetime(xx[2], format='%d.%m.%Y'), "time": xx[3]} # final Y-M-D
            fullData.append(tempDict)

        item['seasonData'] = fullData
        return item




            



