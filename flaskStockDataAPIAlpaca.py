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

    # parsing date string to datetime type
    date = datetime.strptime(date_string, '%d/%m/%Y').date()
    start_date = datetime(date.year, date.month, date.day)
    end_date = datetime.now().date()

    client = StockHistoricalDataClient(api_key, api_secret)
    request_params = StockBarsRequest(
        symbol_or_symbols=[ticker],
        timeframe=TimeFrame.Day,
        start=start_date.strftime('%Y-%m-%d %H:%M:%S'),
        end=end_date.strftime('%Y-%m-%d %H:%M:%S')
    )
    bars = client.get_stock_bars(request_params)
    
    bars_df = bars.df

    # Convert DataFrame to JSON
    date_filter_json = bars_df.reset_index(drop=True).to_json(orient='records')

    return jsonify(date_filter_json)

if __name__ == '__main__':
    app.run()
