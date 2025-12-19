# This is the trading system descived in:
# The Two Moving Averages That Turned $100K Into $1M
# by RB Trading
# https://medium.com/inside-the-trade/the-two-moving-averages-that-turned-100k-into-1m-606a79e99641
#
# Rules:
# Rule #1: Confirm The Uptrend First
# Before you consider any purchase, verify that price is trading above 
# BOTH the 8-day EMA AND the 21-day EMA simultaneously.
#
# Rule #2: Never Chase — Wait For The Pullback
# - Scenario A — The 8-Day EMA Touch
# - Scenario B — The 21-Day EMA Touch
#
# Rule #3: Look For Confirmation Signals
# - Volume should be light on the pullback (sellers are exhausted)
# - A bullish reversal candle should form at the EMA (buyers stepping in)
# - The EMA itself should be sloping upward (trend still healthy)
# - Price should not break below the EMA with conviction
#
# Rule #4: The Non-Negotiable Exit Rule
# If a stock breaks below BOTH the 8-day and 21-day EMAs with a decisive close, 
# the trend is broken. Exit immediately.

import argparse
from backtesting import Backtest, Strategy
import quantstats as qs
import matplotlib.pyplot as plt


from get_quotes import get_quotes
from add_indicators import calc_ema, mean_volume

class EMAStrategy821(Strategy):


    trade_no = 0
    fee = 9.95

    def init(self):
        self.ema8 = self.I(
            lambda: self.data.ema_8,
            name="EMA 8",
            overlay=True
        )

        self.ema21 = self.I(
            lambda: self.data.ema_21,
            name="EMA 21",
            overlay=True
        )

    def next(self):

        ema8_yesterday = self.data.ema_8[-1]
        ema21_yesterday = self.data.ema_21[-1]

        # Only enter a trade if yesterdays close is above 8 and 21 day EMA:
        if self.data.Close[-1] > ema8_yesterday and self.data.Close[-1] > ema21_yesterday \
            and ema8_yesterday > ema21_yesterday:
            # Only open a position if we are not in the market
            if not self.position:
                all_set_go = 0
                # Rule 3: Check for confirmation:
                # - Volume should be light on the pullback (sellers are exhausted)
                if self.data.vol_mean_21[-1] <= self.data.Volume:
                    all_set_go += 1 
                # - A bullish reversal candle should form at the EMA (buyers stepping in)
                # ignoring this one
                # - The EMA itself should be sloping upward (trend still healthy)
                if self.data.ema_21[-1] > self.data.ema_21[-2]:
                    all_set_go += 1 
                # - Price should not break below the EMA with conviction
                # ignore this one, we are only entering above the EMAs!
                # If confirmation then continue
                if all_set_go == 2:
                    # Rule 2
                    if self.data.Close[-2] <= ema8_yesterday and self.data.Close[-1] > ema8_yesterday:
                        self.buy()
                        return
                    # This rule will never get triggered because of "Only enter a trade..."
                    if self.data.Close[-2] <= ema21_yesterday and self.data.Close[-1] > ema21_yesterday:   
                         self.buy()

        # Rule 4
        if self.position and self.data.Close[-1] <= self.data.ema_8[-1]:
            print("EMA21 breached: exit", self.trade_no)
            self.position.close()
            self.trade_no += 1
            return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Programm to backtest the 8 - 21 EMA pullback trading system.")
    parser.add_argument("-t", "--ticker", type=str, help="Ticker of stock to test")
    args = parser.parse_args()
    ohlc = get_quotes(args.ticker, "5y")
    ohlc = calc_ema(ohlc,8)
    ohlc = calc_ema(ohlc,21)
    ohlc = mean_volume(ohlc, 21)

    bt = Backtest(
        ohlc,
        EMAStrategy821,
        cash=100_000,
        commission=(9.95, 0.0),
        trade_on_close=False,
        exclusive_orders=True,
    )

    stats = bt.run()
    print(stats)
    print(stats['_trades'])

    returns = stats['_equity_curve']['Equity'].pct_change().dropna()
    qs.reports.html(returns, output='report.html')

    # Show interactive plot
    bt.plot()
