class Portfolio():

    """
    Intializes a portfolio object.
    """
    def __init__(self,initialValue,years):

        self.currentValue=initialValue
        self.currentStock=0

        self.portionToBuy=0.10
    
        self.years=years

        self.portfolioValueList=[self.currentValue]
        self.portfolioStockList=[self.currentStock]
    
    """
    Calculates the total return of the algorithm over the time period.
    """
    def _TotalReturn(self):
        return round(((self.portfolioValueList[-1]-self.portfolioValueList[0])/(self.portfolioValueList[0]))*100,2)
    
    """
    Calculates the annulaized return of the algorithm over the time period.
    """
    def _AnnualizedReturn(self):
        return round((((self.portfolioValueList[-1]/self.portfolioValueList[0])**(1/self.years)-1)*100),2)

    """
    Spend a portion of the current portfolio value on new stock.
    """
    def buy(self,closePrice):
        if self.currentValue>0:
            stock=(self.currentValue*0.1)//closePrice
            price=stock*closePrice

            self.currentStock+=stock
            self.currentValue-=price

        self.portfolioValueList.append(self.currentValue)
        self.portfolioStockList.append(self.currentStock)
    
    """
    Liquidates all current stock.
    """
    def sell(self,closePrice):
        if self.currentStock>0:
            self.currentValue+=closePrice*self.currentStock
            self.currentStock=0
    
        self.portfolioValueList.append(self.currentValue)
        self.portfolioStockList.append(self.currentStock)
    
    """
    Prints each stattistic calculated for the current portfolio.
    """
    def printStatistics(self):
        statistics={"Initial Portfolio Value: ": round(self.portfolioValueList[0],2), 
                    "Final Portfolio Value ": round(self.portfolioValueList[-1],2),
                    "Total Return: ": self._TotalReturn(), 
                    "Annualized Return (CAGR): ": self._AnnualizedReturn()}

        print("-----Statistics-----")

        for statistic,value in statistics.items():
            print(statistic + str(value))