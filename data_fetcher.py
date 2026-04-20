import yfinance as yf

def get_prices(tickers):
    data = yf.download(tickers, period="6mo", interval="1d")["Close"]
    return data.ffill()