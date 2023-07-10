from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient

import os
import pandas as pd

client = StockHistoricalDataClient(api_key, api_secret)
request_params = StockBarsRequest(
                        symbol_or_symbols=["AAPL"],
                        timeframe=TimeFrame.Day,
                        start="2022-10-04 00:00:00",
                        end="2022-10-06 00:00:00"
                 )
bars = client.get_stock_bars(request_params)
bars_df = bars.df

print(bars_df)