import pandas as pd
from datetime import date, timedelta
import yfinance as yf
import random, os
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt


class Backtester():
    def __init__(self):
        
        self.symbols=self._getSymbols()
    
        self.startDate=date.today()-relativedelta(years=10)
        self.endDate=date.today()

        self.interdayData=self._getData(self.startDate,self.endDate)


    def _getSandP500SymbolsCSV(self,OutURL):
        URL="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        companyDataIndex=0

        html=pd.read_html(URL)

        companyData=html[companyDataIndex]

        companyData["Symbol"].to_csv(OutURL,index=False)

    
    def _getSymbols(self):
        URL="SandP500Symbols.csv"
        self._getSandP500SymbolsCSV(URL)
        symbolsCSV=pd.read_csv(URL)
        symbolsList=symbolsCSV['Symbol'].tolist()
        return [s.replace('.', '-') for s in symbolsList]
    
    
    def _getClosingPrice(self,company,date):
        dateKey=pd.Timestamp(date)
        return self.interdayData.loc[dateKey, ("Close",company)]
    
    
    def _getDateString(self,date):
        return str(date.year)+"-"+str(date.month)+"-"+str(date.day)
    

    def _getData(self,startDate,endDate):
        fileName="SandP500CSV.csv"
        startDateString=self._getDateString(startDate)
        endDateString=self._getDateString(endDate)
        if not os.path.isfile(fileName):
            data=yf.download(self.symbols,startDateString,endDateString)
            data.to_csv(fileName)
            return data
        else:
            return pd.read_csv("SandP500CSV.csv",header=[0,1],index_col=0,parse_dates=True,low_memory=False)
    
    
    #todo Change selection of companies as some do not have stocks on start date
    #todo change 10 to a variable somehow
    def algorithmSimulation(self,algorithm):
        randomCompanies=[self.symbols[random.randint(0,len(self.symbols))] for _ in range(3)]

        buySellTrendperCompany={}
        
        for company in randomCompanies:
            date=self.startDate+relativedelta(years=1)
            buySellTrend={}
            while date!=self.endDate+timedelta(days=1):
                if pd.Timestamp(date) in self.interdayData.index:
                    closePrice=self._getClosingPrice(company,date)
                    buySellTrend[pd.Timestamp(date)]=algorithm(closePrice)
                    
                date+=timedelta(days=1)

            buySellTrendperCompany[company]=buySellTrend
        
        return buySellTrendperCompany

    
    def plotBuySellTrends(self, buySellTrendperCompany):
        for company, buySellTrend in buySellTrendperCompany.items():
            plt.figure(figsize=(12, 6))
            plt.plot(self.interdayData.index, self.interdayData[("Open", company)], label="Open Price", color="blue")

            for date, signal in buySellTrend.items():
                price = self.interdayData.loc[date, ("Open", company)]
                if signal == 1:
                    plt.scatter(date, price, color="green", marker="^", s=50, label="Buy" if "Buy" not in plt.gca().get_legend_handles_labels()[1] else "")
                elif signal == -1:
                    plt.scatter(date, price, color="orange", marker="v", s=50, label="Sell" if "Sell" not in plt.gca().get_legend_handles_labels()[1] else "")

            plt.title(f"{company} Open Price Over Time with Buy/Sell Indicators")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.legend()
            plt.grid(True)
            plt.show()

