import yfinance as yf

def get_prices():

    assets = {
        "brent": "BZ=F",
        "wti": "CL=F",
        "gold": "GC=F",
        "sp500": "^GSPC",
        "nasdaq": "^IXIC"
    }

    prices = {}

    for name, ticker in assets.items():
        data = yf.Ticker(ticker).history(period="1d")
        prices[name] = float(data["Close"].iloc[-1])

    return prices