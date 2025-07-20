# Backtesting Trading Strategies

This project implements and backtests a variety of algorithmic trading strategies using Python. The goal is to test how different strategies would have performed historically using a sliding window of price data.

---

## Project Structure

### `strategies/`
Contains modular implementations of trading strategies.

### `backtesting/backtesting.py`
Core framework that simulates and visualizes how strategies would have performed on real historical market data.

---

## Strategies Implemented

### 1. **SMA Crossover Strategy**
- **Type**: Trend-following  
- **Logic**:  
  - Uses a short-term (50-day) and long-term (200-day) Simple Moving Average (SMA).  
  - **Buy** signal when short-term SMA crosses above long-term SMA.  
  - **Sell** signal when short-term SMA crosses below long-term SMA.  
- **Maintains**: A rolling list of 200 prices for efficient SMA calculation.

### 2. **Mean Reversion Strategy**
- **Type**: Mean reversion  
- **Logic**:  
  - Uses a 20-day SMA to estimate a "fair" price.  
  - **Buy** when price is below the SMA.  
  - **Sell** when price is above the SMA.  
- **Maintains**: A rolling list of 20 prices.

### 3. **Momentum Breakout Strategy**
- **Type**: Momentum  
- **Logic**:  
  - Tracks the highest and lowest prices over the past 20 days (excluding the current price).  
  - **Buy** if the current price breaks above the recent high.  
  - **Sell** if it breaks below the recent low.  
- **Maintains**: A rolling list of 20 prices and ignores the most recent value in comparisons.

---

## Backtesting Framework

The `Backtester` class (`backtesting/backtesting.py`) is responsible for:

- Downloading and caching historical data for all S&P 500 companies.
- Randomly selecting a subset of companies for simulation.
- Running a chosen trading strategy on daily closing prices over a 10-year period.
- Plotting buy/sell signals alongside historical stock prices for visualization.

### Key Methods

- `algorithmSimulation(algorithm)`: Runs the given strategy on multiple companies and returns buy/sell signals by date.
- `plotBuySellTrends(result)`: Plots stock price with overlayed buy/sell signals.

---

## Authors

- **Evan Phillips**  
- **Whitt Byrd**
