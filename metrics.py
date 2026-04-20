import numpy as np
import pandas as pd


def calculate_portfolio_value(prices, portfolio):
    total_value = 0
    pnl = 0

    for ticker, info in portfolio.items():
        latest_price = prices[ticker].iloc[-1]
        qty = info["qty"]
        buy_price = info["buy_price"]

        total_value += qty * latest_price
        pnl += qty * (latest_price - buy_price)

    return total_value, pnl


def calculate_returns(prices):
    returns = prices.pct_change().dropna()
    return returns


def calculate_volatility(returns):
    return returns.std() * np.sqrt(252)


def calculate_var(returns, confidence=0.95):
    portfolio_returns = returns.mean(axis=1)
    var = np.percentile(portfolio_returns, (1 - confidence) * 100)
    return var


def calculate_drawdown(prices):
    portfolio_curve = prices.mean(axis=1)
    running_max = portfolio_curve.cummax()
    drawdown = (portfolio_curve - running_max) / running_max
    return drawdown


def stress_test(value, shock=-0.07):
    stressed_value = value * (1 + shock)
    loss = value - stressed_value
    return stressed_value, loss