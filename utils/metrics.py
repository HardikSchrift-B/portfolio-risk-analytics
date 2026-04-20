import numpy as np


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
    return prices.pct_change().dropna()


def calculate_volatility(returns):
    return returns.std() * np.sqrt(252)


def calculate_var(returns, confidence=0.95):
    portfolio_returns = returns.mean(axis=1)

    return np.percentile(
        portfolio_returns,
        (1 - confidence) * 100
    )


def calculate_drawdown(prices):
    portfolio_curve = prices.mean(axis=1)

    running_max = portfolio_curve.cummax()

    drawdown = (
        portfolio_curve - running_max
    ) / running_max

    return drawdown


def stress_test(value, shock=-0.07):
    stressed_value = value * (1 + shock)

    loss = value - stressed_value

    return stressed_value, loss


def calculate_sharpe_ratio(
    returns,
    risk_free_rate=0.02
):
    portfolio_returns = returns.mean(axis=1)

    excess_returns = (
        portfolio_returns - risk_free_rate / 252
    )

    sharpe = (
        excess_returns.mean()
        / excess_returns.std()
    ) * np.sqrt(252)

    return sharpe


def calculate_beta(
    returns,
    market_returns
):
    portfolio_returns = returns.mean(axis=1)

    # Convert market data to Series if needed
    if hasattr(market_returns, "squeeze"):
        market_returns = market_returns.squeeze()

    # Align same dates
    portfolio_returns, market_returns = portfolio_returns.align(
        market_returns,
        join="inner"
    )

    # Convert to arrays
    portfolio_returns = portfolio_returns.values
    market_returns = market_returns.values

    covariance = np.cov(
        portfolio_returns,
        market_returns
    )[0][1]

    variance = np.var(market_returns)

    if variance == 0:
        return 0

    beta = covariance / variance

    return beta