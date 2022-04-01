# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import os.path

class MlfootballpredictionPipeline:

    def open_spider(self, spider):

       self.Matches = []

    def process_item(self, item, spider):

        self.Matches+=item['seasonData']

    def close_spider(self, spider):

       fullDataFrame = pd.DataFrame(self.Matches)

       folderPath = os.getcwd().split("/")
       folderPath = "/".join(folderPath[:-2])

       if spider.name == "previousMatches":
         fullDataFrame.sort_values(by=['date'],  inplace=True, ascending=False)
         fullDataFrame.to_csv(folderPath + "/finalData.csv", sep=",", index = False)

       if spider.name == "nextMatches":
         fullDataFrame.sort_values(by=['date', 'time'],  inplace=True, ascending= (True, True) )
         fullDataFrame.to_csv(folderPath + "/games.csv", sep=",", index = False)


