import pandas as pd
from datetime import date, timedelta
import yfinance as yf
import random, os
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt


class Backtester():
    """
    Creates a backtesting object for testing and visualizing different trading algorithms performances over random S&P500 companies.
    """

    def __init__(self):
        """
        Initializes the Backtester object. Scrapes wikipedia for S&P500 companies and uses yahoo finance to gather stock
        data for all companies over the last 10 years. Gathers this data in a panda dataframe.
        """

        self.symbols=self._getSymbols()
    
        self.startDate=date.today()-relativedelta(years=10)
        self.endDate=date.today()

        self.interdayData=self._getData(self.startDate,self.endDate)


    def _getSandP500SymbolsCSV(self,OutURL):
        """
        Scrapes wikipedia for all S&P500 companies' symbols. Writes all of these to a CSV file.
        """

        URL="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        companyDataIndex=0

        html=pd.read_html(URL)

        companyData=html[companyDataIndex]

        companyData["Symbol"].to_csv(OutURL,index=False)

    
    def _getSymbols(self):
        """
        Reads from the symbols CSV and places all symbols in a list with the correct yahoo finance format.
        """

        URL="SandP500Symbols.csv"
        self._getSandP500SymbolsCSV(URL)
        symbolsCSV=pd.read_csv(URL)
        symbolsList=symbolsCSV['Symbol'].tolist()
        return [s.replace('.', '-') for s in symbolsList]
    
    
    def _getClosingPrice(self,company,date):
        """
        Finds the closing stock price of a company on a given date.
        """

        dateKey=pd.Timestamp(date)
        return self.interdayData.loc[dateKey, ("Close",company)]
    
    
    def _getDateString(self,date):
        """
        Returns the date as a string. Used for yahoo finance.
        """

        return str(date.year)+"-"+str(date.month)+"-"+str(date.day)
    

    def _getData(self,startDate,endDate):
        """
        Gathers the stock price data. If the CSV is already present witht he data, it imports it.
        If not, it downloads the data from yahoo finance and writes it to a csv. Returns the data.
        """

        fileName="SandP500CSV.csv"
        startDateString=self._getDateString(startDate)
        endDateString=self._getDateString(endDate)
        if not os.path.isfile(fileName):
            data=yf.download(self.symbols,startDateString,endDateString)
            data.to_csv(fileName)
            return data
        else:
            return pd.read_csv("SandP500CSV.csv",header=[0,1],index_col=0,parse_dates=True,low_memory=False)
    
    
    def _plotBuySellTrends(self, buySellTrendperCompany):
        """
        Uses matplotlib to plot the stock opening price over time for a give company. Also plots arrow indicators
        over 1 month periods for what the used algorithm generally did over that month, either buy sell or hold.
        """

        for company, buySellTrend in buySellTrendperCompany.items():
            plt.figure(figsize=(12, 6))
            plt.plot(self.interdayData.index, self.interdayData[("Open", company)], label="Open Price", color="blue")

            for date, signal in buySellTrend.items():
                if pd.Timestamp(date) in self.interdayData.index:
                    openPrice=self.interdayData.loc[pd.Timestamp(date), ("Open", company)]
                    if signal>=1:
                        plt.scatter(date, openPrice, color="green", marker="^", s=200, label="Buy" if "Buy" not in plt.gca().get_legend_handles_labels()[1] else "")
                    elif signal<=-1:
                        plt.scatter(date, openPrice, color="orange", marker="v", s=200, label="Sell" if "Sell" not in plt.gca().get_legend_handles_labels()[1] else "")

            plt.title(f"{company} Open Price Over Time with Buy/Sell Indicators")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.legend()
            plt.grid(True)
            plt.show()
    

    def algorithmSimulation(self,algorithm,numOfCompanies):
        """
        Runs a simulation of an algorithm for some number of companies over the last ten years. Records what the algorithm decides to do
        each day. This data is then plotted.
        """

        randomCompanies=[self.symbols[random.randint(0,len(self.symbols))] for _ in range(numOfCompanies)]
        offsetMonths=1

        buySellTrendperCompany={}
        
        for company in randomCompanies:
            date=self.startDate+relativedelta(years=1)
            cutoffDate=date+relativedelta(months=offsetMonths)
            buySellTrend={date:0}
            while date!=self.endDate+timedelta(days=1):
                if pd.Timestamp(date) in self.interdayData.index:
                    closePrice=self._getClosingPrice(company,date)
                    buySellTrend[cutoffDate-relativedelta(months=offsetMonths)]+=algorithm(closePrice)
                if date==cutoffDate:
                    cutoffDate=date+relativedelta(months=offsetMonths)
                    buySellTrend[date]=0
                    
                date+=timedelta(days=1)

            buySellTrendperCompany[company]=buySellTrend
        
        self._plotBuySellTrends(buySellTrendperCompany)
