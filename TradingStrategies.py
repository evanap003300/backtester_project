class MeanReversionStrategy():
    def __init__(self):
        self.pastPrices=[]

    # Get the original 20-period SMA and then keep updating it in a cache for efficent lookups
    def signal(self,closePrice):
        # SMA Period
        SMA_PERIOD = 20
        
        if (len(self.pastPrices) < SMA_PERIOD):
            self.pastPrices.append(closePrice)
            return 0 # Not enough data to make a decision
        
        # Add the new price to the top of the list
        self.pastPrices.pop(0)
        self.pastPrices.append(closePrice)

        # Calculate SMA
        SMASum = 0
        for i in range(0, SMA_PERIOD, 1):
            SMASum += self.pastPrices[i]
        
        SMAPrice = SMASum / SMA_PERIOD

        if closePrice < SMAPrice:
            return 1 # Buy 
        
        if closePrice > SMAPrice:
            return -1 # Sell 
        
        return 0 # Hold 
    
class MomentumBreakoutStrategy():
    def __init__(self):
        self.pastPrices=[]
    
    def signal(self,closePrice):
        # Number of days to look back for recent high/low
        LOOKBACK_PERIOD = 20
        
        if (len(self.pastPrices) < LOOKBACK_PERIOD):
            self.pastPrices.append(closePrice)
            return 0 # Not enough data to make a decision
        
        # Add the new price to the top of the list
        self.pastPrices.pop(0)
        self.pastPrices.append(closePrice)

        max_price = 0
        min_price = float('inf')

        for i in range(0, LOOKBACK_PERIOD - 1, 1):
            if self.pastPrices[i] > max_price:
                max_price = self.pastPrices[i]
            if self.pastPrices[i] < min_price:
                min_price = self.pastPrices[i]

        if closePrice < min_price:
            return -1 # Sell 
        
        if closePrice > max_price:
            return 1 # Buy 
        
        return 0 # Hold
    
class SMACrossoverStrategy():
    def __init__(self):
        self.pastPrices=[]
    
    def signal(self,closePrice):
        # SMA Periods 
        SHORT_TERM_SMA_PERIOD = 50
        LONG_TERM_SMA_PERIOD = 200
        
        if (len(self.pastPrices) < LONG_TERM_SMA_PERIOD):
            self.pastPrices.append(closePrice)
            return 0 # Not enough data to make a decision
        
        # Add the new price to the top of the list
        self.pastPrices.pop(0)
        self.pastPrices.append(closePrice)

        # Calculate short-term SMA
        short_term_sma_sum = 0
        for i in range(LONG_TERM_SMA_PERIOD - SHORT_TERM_SMA_PERIOD, LONG_TERM_SMA_PERIOD, 1):
            short_term_sma_sum += self.pastPrices[i]
        
        short_term_sma_price = short_term_sma_sum / SHORT_TERM_SMA_PERIOD
        
        # Calculate long-term SMA
        long_term_sma_sum = 0
        for i in range(0, LONG_TERM_SMA_PERIOD, 1):
            long_term_sma_sum += self.pastPrices[i]
        
        long_term_sma_price = long_term_sma_sum / LONG_TERM_SMA_PERIOD
        
        if short_term_sma_price > long_term_sma_price:
            return 1 # Buy
        
        if short_term_sma_price < long_term_sma_price:
            return -1 # Sell
        
        return 0 # Hold 