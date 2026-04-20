import streamlit as st
import plotly.express as px

from utils.data_fetcher import get_prices, get_market_data
from utils.metrics import (
    calculate_portfolio_value,
    calculate_returns,
    calculate_volatility,
    calculate_var,
    calculate_drawdown,
    stress_test,
    calculate_sharpe_ratio,
    calculate_beta
)

st.set_page_config(page_title="Portfolio Risk Dashboard", layout="wide")

st.title("📊 Real-Time Portfolio Risk Analytics Dashboard")

portfolio = {
    "AAPL": {"qty": 10, "buy_price": 170},
    "TSLA": {"qty": 5, "buy_price": 250},
    "JPM": {"qty": 8, "buy_price": 140},
    "MSFT": {"qty": 6, "buy_price": 300}
}

tickers = list(portfolio.keys())

prices = get_prices(tickers)
market_prices = get_market_data()

value, pnl = calculate_portfolio_value(prices, portfolio)

returns = calculate_returns(prices)
market_returns = market_prices.pct_change().dropna()

volatility = calculate_volatility(returns)
var = calculate_var(returns)
drawdown = calculate_drawdown(prices)

stressed_value, loss = stress_test(value)

sharpe = calculate_sharpe_ratio(returns)
beta = calculate_beta(returns, market_returns)

# --------------------------
# TOP METRICS
# --------------------------
st.subheader("💼 Portfolio Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Portfolio Value ($)", round(value, 2))
col2.metric("Total P&L ($)", round(pnl, 2))
col3.metric("Annual Volatility", round(volatility.mean(), 4))
col4.metric("95% VaR", round(var, 4))

# --------------------------
# ADVANCED METRICS
# --------------------------
st.subheader("📊 Advanced Risk Metrics")

col5, col6 = st.columns(2)

col5.metric("Sharpe Ratio", round(sharpe, 3))
col6.metric("Beta vs S&P 500", round(beta, 3))

# --------------------------
# PRICE HISTORY
# --------------------------
st.subheader("📈 Price History")
st.line_chart(prices)

# --------------------------
# RETURN CURVE
# --------------------------
st.subheader("📈 Portfolio Return Curve")

portfolio_returns = returns.mean(axis=1)
cumulative_returns = (1 + portfolio_returns).cumprod()

st.line_chart(cumulative_returns)

# --------------------------
# CORRELATION
# --------------------------
st.subheader("🔗 Correlation Matrix")

corr = returns.corr()

fig = px.imshow(corr, text_auto=True, aspect="auto")
st.plotly_chart(fig, use_container_width=True, key="heatmap")

# --------------------------
# DRAWDOWN
# --------------------------
st.subheader("📉 Drawdown")
st.line_chart(drawdown)

# --------------------------
# STRESS TEST
# --------------------------
st.subheader("💣 Stress Test")

col7, col8 = st.columns(2)

col7.metric("Stressed Value ($)", round(stressed_value, 2))
col8.metric("Loss ($)", round(loss, 2))