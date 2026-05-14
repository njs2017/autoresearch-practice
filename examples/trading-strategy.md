# AutoResearch — Trading Strategy Optimization

## Overview
You are optimizing a trading strategy's performance on historical data.
The agent modifies `target.py` (strategy logic) and backtests evaluate it.

## Domain Configuration
- **Domain**: Quantitative trading strategy
- **Target file**: `target.py` (strategy: signals, entry/exit rules, sizing)
- **Eval command**: `python evaluate.py`
- **Metric name**: `score` (negative Sharpe ratio — lower is better)
- **Time budget per run**: 2 minutes (backtest on fixed historical window)

## What You CAN Do
- Change entry/exit signal logic
- Modify position sizing
- Add/remove technical indicators
- Change lookback periods, thresholds
- Add risk management rules (stop-loss, take-profit)
- Combine multiple signals

## What You CANNOT Do
- Modify `evaluate.py` (the backtester)
- Look ahead in the data (no future data leakage!)
- Change the historical data window
- Add transaction costs below the configured rate

## Strategy Hints
- Simple strategies often beat complex ones out-of-sample
- Beware overfitting: if it looks too good, it probably is
- Robust improvements: works across multiple sub-periods
- Risk management often matters more than entry signals
- Fewer trades with higher conviction > many noisy trades

## ⚠️ REWARD HACKING WARNING
The agent may find ways to "game" the metric without real improvement.
Watch for: curve-fitting to specific dates, excessive parameter tuning,
strategies that only work on the exact test window.
