import numpy as np
import scrapy
from MLfootballPrediction.items import MlfootballpredictionItem
import pandas as pd
from datetime import datetime, timedelta

class getMatchesSpider(scrapy.Spider):
    name = "previousMatches"

    def start_requests(self):

        urls = [
            'https://www.betexplorer.com/soccer/norway/eliteserien/results/',
            'https://www.betexplorer.com/soccer/norway/eliteserien-2020/results/',
            'https://www.betexplorer.com/soccer/norway/eliteserien-2019/results/',
            #'https://www.betexplorer.com/soccer/norway/eliteserien-2018/results/'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        item = MlfootballpredictionItem()

        # matches, results, odds and time 
        matches = np.array(response.xpath('//td[@class="h-text-left"]/a/span/text() | //td[@class="h-text-left"]/a/span/strong/text()').extract())
        matches.shape = (int(len(matches)/2), 2)
        result = np.array(response.xpath('//td[@class="h-text-center"]/a/text()').extract())

        # formating date
        date =  response.xpath('//td[@class="h-text-right h-text-no-wrap"]/text()').extract()
        year =  datetime.today().strftime('%Y')
        yesterday0 = datetime.now() - timedelta(1)
        yesterday = str(yesterday0.day) + "." + str(yesterday0.month) + "." + str(yesterday0.year)

        for cDate in date:
            if len(cDate)==6:
              date[date.index(cDate)] = cDate + year
            if cDate == "Yesterday":  
              date[date.index(cDate)] = yesterday


        odds = np.array(response.xpath('//td[@class="table-main__odds"]/@data-odd | //td[@class="table-main__odds colored"]/span/span/span/@data-odd').extract())
        odds.shape = (len(matches), 3)
        
        DATA = list(zip(matches, result, odds, date))

        fullData = []
        for xx in DATA:
          tempDict = {"homeTeam": xx[0][0], "awayTeam": xx[0][1], "result": xx[1], "odds": list(xx[2]), "date": pd.to_datetime(xx[3], format='%d.%m.%Y')} # final Y-M-D
          fullData.append(tempDict)

        item['seasonData'] = fullData
        return item


