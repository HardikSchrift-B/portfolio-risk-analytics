import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.data_fetcher import get_prices
from utils.metrics import (
    calculate_portfolio_value,
    calculate_returns,
    calculate_volatility,
    calculate_var,
    calculate_drawdown,
    stress_test
)

# -----------------------------
# Portfolio Holdings
# -----------------------------
portfolio = {
    "AAPL": {"qty": 10, "buy_price": 170},
    "TSLA": {"qty": 5, "buy_price": 250},
    "JPM": {"qty": 8, "buy_price": 140},
    "MSFT": {"qty": 6, "buy_price": 300}
}

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Portfolio Risk Dashboard",
    layout="wide"
)

st.title("📊 Real-Time Portfolio Risk Dashboard")

# -----------------------------
# Get Data
# -----------------------------
tickers = list(portfolio.keys())
prices = get_prices(tickers)

# -----------------------------
# Core Metrics
# -----------------------------
value, pnl = calculate_portfolio_value(prices, portfolio)

returns = calculate_returns(prices)
volatility = calculate_volatility(returns)
var = calculate_var(returns)

drawdown = calculate_drawdown(prices)

stressed_value, loss = stress_test(value)

# -----------------------------
# Top Metrics Row
# -----------------------------
st.subheader("💼 Portfolio Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Portfolio Value ($)", round(value, 2))

with col2:
    st.metric("Total P&L ($)", round(pnl, 2))

with col3:
    st.metric("Annual Volatility", round(volatility.mean(), 4))

with col4:
    st.metric("95% VaR", round(var, 4))

# -----------------------------
# Price Chart
# -----------------------------
st.subheader("📈 Price History")
st.line_chart(prices)

# -----------------------------
# Correlation Heatmap
# -----------------------------
st.subheader("🔗 Correlation Matrix")

corr = returns.corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Asset Correlation Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="corr_heatmap"
)

# -----------------------------
# Drawdown Chart
# -----------------------------
st.subheader("📉 Drawdown")
st.line_chart(drawdown)

# -----------------------------
# Stress Test
# -----------------------------
st.subheader("💣 Stress Test (-7% Market Shock)")

col5, col6 = st.columns(2)

with col5:
    st.metric(
        "Stressed Portfolio Value ($)",
        round(stressed_value, 2)
    )

with col6:
    st.metric(
        "Estimated Loss ($)",
        round(loss, 2)
    )

# -----------------------------
# Recent Prices Table
# -----------------------------
st.subheader("📋 Recent Prices")
st.dataframe(prices.tail())