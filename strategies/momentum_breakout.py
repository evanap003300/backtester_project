# Number of days to look back for recent high/low
LOOKBACK_PERIOD = 20

# keeps an array of 20 prices 
past_prices = []

# If we reach higher highs or lower lows than the previous 20 days, we will buy or sell

# Get the original 20-period SMA and then keep updating it in a cache for efficent lookups
def momentum_breakout_strategy(close_price: int) -> int:
    global past_prices
    
    if (len(past_prices) < LOOKBACK_PERIOD):
        past_prices.append(close_price)
        return 0 # Not enough data to make a decision
    
    # Add the new price to the top of the list
    past_prices.pop(0)
    past_prices.append(close_price)

    max_price = 0
    min_price = float('inf')

    for i in range(0, LOOKBACK_PERIOD - 1, 1):
        if past_prices[i] > max_price:
            max_price = past_prices[i]
        if past_prices[i] < min_price:
            min_price = past_prices[i]

    if close_price < min_price:
        return -1 # Sell 
    
    if close_price > max_price:
        return 1 # Buy 
    
    return 0 # Hold 