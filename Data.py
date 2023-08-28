import yfinance as yf

def get_historical_data(symbol: str):
    return yf.Ticker(symbol).history(period="max")


if __name__ == '__main__':
    print(get_historical_data('AAPL'))