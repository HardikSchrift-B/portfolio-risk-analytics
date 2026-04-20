import yfinance as yf


def get_prices(tickers):
    data = yf.download(
        tickers,
        period="6mo",
        interval="1d"
    )["Close"]

    return data.ffill()


def get_market_data():
    market = yf.download(
        "^GSPC",
        period="6mo",
        interval="1d"
    )["Close"]

    return market.ffill()