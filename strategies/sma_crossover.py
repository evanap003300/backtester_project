# Start date 
SHORT_TERM_SMA_PERIOD = 50
LONG_TERM_SMA_PERIOD = 200

# Gets start date for the strategy

# keep an array of 200 prices 

# start the top from most recent 
# update top elemeent of the array each time with the new price 
# Need to remove from bottom and add to top

past_prices = []

# Get the original 200-period SMA and then keep updating it in a cache for efficent lookups 

# Assumes data is list of past prices in chronological order with 200 prices of data
def sma_crossover_strategy(close_price: int) -> int:
    global past_prices
    
    if (len(past_prices) < LONG_TERM_SMA_PERIOD):
        past_prices.append(close_price)
        return 0 # Not enough data to make a decision
    
    # Add the new price to the top of the list
    past_prices.pop(0)
    past_prices.append(close_price)

    # Calculate short-term SMA
    short_term_sma_sum = 0
    for i in range(LONG_TERM_SMA_PERIOD - SHORT_TERM_SMA_PERIOD, LONG_TERM_SMA_PERIOD, 1):
        short_term_sma_sum += past_prices[i]
    
    short_term_sma_price = short_term_sma_sum / SHORT_TERM_SMA_PERIOD
    
    # Calculate long-term SMA
    long_term_sma_sum = 0
    for i in range(0, LONG_TERM_SMA_PERIOD, 1):
        long_term_sma_sum += past_prices[i]
    
    long_term_sma_price = long_term_sma_sum / LONG_TERM_SMA_PERIOD
    
    if short_term_sma_price > long_term_sma_price:
        return 1 # Buy
    
    if short_term_sma_price < long_term_sma_price:
        return -1 # Sell
    
    return 0 # Hold 

for i in range(0, 500):
    print(sma_crossover_strategy(i))