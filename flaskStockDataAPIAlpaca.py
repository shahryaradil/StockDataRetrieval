from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
from alpaca.data.timeframe import TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical import StockHistoricalDataClient

app = Flask(__name__)

@app.route('/stock-data', methods=['GET'])
def get_stock_data():
    ticker = request.args.get('ticker')
    date_string = request.args.get('date')

    date = datetime.strptime(date_string, '%d/%m/%Y').date()
    start_date = datetime(date.year, date.month, date.day)
    end_date = datetime.now().date()

    api_key = ''
    api_secret = ''

    client = StockHistoricalDataClient(api_key, api_secret)

    # Fetch adjusted data
    adjusted_request_params = StockBarsRequest(
        symbol_or_symbols=[ticker],
        timeframe=TimeFrame.Day,
        start=start_date.strftime('%Y-%m-%d %H:%M:%S'),
        end=end_date.strftime('%Y-%m-%d %H:%M:%S'),
        adjustment='all'
    )
    adjusted_bars = client.get_stock_bars(adjusted_request_params)
    adjusted_bars_df = adjusted_bars.df

    # Fetch unadjusted data
    unadjusted_request_params = StockBarsRequest(
        symbol_or_symbols=[ticker],
        timeframe=TimeFrame.Day,
        start=start_date.strftime('%Y-%m-%d %H:%M:%S'),
        end=end_date.strftime('%Y-%m-%d %H:%M:%S')
    )
    unadjusted_bars = client.get_stock_bars(unadjusted_request_params)
    unadjusted_bars_df = unadjusted_bars.df

    # Rename adjusted columns
    adjusted_bars_df.rename(columns={
        'open': 'adjusted_open',
        'close': 'adjusted_close',
        'high': 'adjusted_high',
        'low': 'adjusted_low'
    }, inplace=True)

    # Combine adjusted and unadjusted dataframes
    combined_df = pd.concat([unadjusted_bars_df, adjusted_bars_df[['adjusted_open', 'adjusted_close', 'adjusted_high', 'adjusted_low']]], axis=1)

    combined_json = combined_df.reset_index(drop=True).to_json(orient='records')

    return jsonify(combined_json)

if __name__ == '__main__':
    app.run()
