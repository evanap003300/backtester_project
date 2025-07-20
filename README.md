# Backtesting Trading Strategies

This project implements and backtests a variety of algorithmic trading strategies using Python. The goal is to test how different strategies would have performed historically using a sliding window of price data.

## 📈 Strategies Implemented

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

## 🔁 Structure
Each strategy function:
- Receives the latest price (`close_price`)
- Maintains its own internal rolling window of past prices
- Returns:
  - `1` → Buy
  - `-1` → Sell
  - `0` → Hold

## 🚧 Next Steps
- Combine strategies into a unified backtester.
- Add backtesting logic to simulate trades, profit/loss, and visualization.
- Evaluate strategy performance using metrics like Sharpe Ratio, drawdown, and win rate.

## 📎 Notes
- Each strategy is stateless across sessions unless modified — state is tracked via global lists.
- Be cautious when scaling — consider converting to class-based or vectorized implementations for efficiency.

---

**Author**: Evan Phillips  
**Last updated**: Summer 2025
