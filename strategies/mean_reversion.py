# SMA Period
SMA_PERIOD = 20

# keeps an array of 20 prices 
past_prices = []

# Get the original 20-period SMA and then keep updating it in a cache for efficent lookups
def mean_reversion_strategy(close_price: int) -> int:
    global past_prices
    
    if (len(past_prices) < SMA_PERIOD):
        past_prices.append(close_price)
        return 0 # Not enough data to make a decision
    
    # Add the new price to the top of the list
    past_prices.pop(0)
    past_prices.append(close_price)

    # Calculate SMA
    sma_sum = 0
    for i in range(0, SMA_PERIOD, 1):
        sma_sum += past_prices[i]
    
    sma_price = sma_sum / SMA_PERIOD

    if close_price < sma_price:
        return 1 # Buy 
    
    if close_price > sma_price:
        return -1 # Sell 
    
    return 0 # Hold 
