import pandas as pd

def get_66_day_sma(quotes):
    # Function to calculate the 66 day SMA
    quotes["SMA66"] = quotes["Close"].rolling(window=33).mean()
    return(quotes)

def get_lowest(quotes, days):
    # Function to identify if the current Low is the lowest low in the last days
    quotes["is_lowest_low"] = quotes["Low"] == quotes["Low"].rolling(window=days).min()
    return(quotes)

def calc_ema(prices, period):
    prices[f'ema_{period}'] = prices["Close"].ewm(span=period, adjust=False).mean()
    return prices

def mean_volume(prices, period):
    prices[f'vol_mean_{period}'] = prices["Volume"].rolling(window=period, min_periods=1).mean()
    return prices
