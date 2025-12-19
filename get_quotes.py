import yfinance as yf

def get_quotes(ticker, range):
    # a simple function to get stock quotes from Yahoo Finance
    # returns quotes in Close, High, Low, Open, Volume
    # "2y" - 2 years
    # "1d" – daily
    # "1wk" – weekly
    # "1mo" – monthly

   dat = yf.Ticker(ticker)
   data = dat.history(period=range, interval="1d")
   return(data)
