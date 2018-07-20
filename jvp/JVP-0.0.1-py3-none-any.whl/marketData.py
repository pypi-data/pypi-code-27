import numpy as np
import eikon as ek
import pandas as pd
import matplotlib.pyplot as plt

class marketData:
    def __init__(self, key, ticker, startDate,endDate, thresold=0.03, parameter = ["TR.BIDPRICE.Date",'TR.BIDPRICE'], provider = "EIKON", numberNews = 1):
        ek.set_app_id(key)
        self.__ticker = ticker
        self.__startDate = startDate
        self.__endDate = endDate
        self.__provider = provider
        self.__parameter = parameter
        self.__numberNews = numberNews
        self.__thresold = thresold
        self.__data = self.getData()
        self.__news = self.getNews()

    def getData(self):
        data = pd.DataFrame(ek.get_data(self.__ticker, self.__parameter,parameters={'SDate':self.__startDate,'EventType':'ALL','EDate':self.__endDate})[0])
        data["thresold"] = np.abs(data['Bid Price'].pct_change().fillna(value=0)) > self.__thresold
        data["news"] = data.apply(lambda x : ek.get_news_headlines(self.__ticker,self.__numberNews,date_from = x['Date'],date_to=str(pd.to_datetime(x['Date'])+pd.DateOffset(days=1)) )['text'] if(x['thresold']) else None,axis=1)
        return data.drop(columns=["thresold"])

    def plot(self,markersize = 1, markerNews = 20, colorUp = 'b',colorDown = 'r'):
        price = self.__data['Bid Price']
        marketNews = self.__data.apply(lambda x: colorUp if (x["news"] == None) else colorDown, axis=1)
        plt.plot(price, colorUp+'o-', markersize = markersize)
        plt.scatter(self.__data['Date'].values, price, c=marketNews, s=markerNews)

    def getNews(self):
        return self.__data.mask(self.__data["news"].eq(None)).dropna()

    @property
    def data(self):
        return self.__data

    @property
    def news(self):
        return self.__news
    @property
    def thresold(self):
        return self.__thresold

    @property
    def nbNews(self):
        return self.__numberNews
    @property
    def parameter(self):
        return self.__parameter
    @property
    def provider(self):
        return self.__provider


