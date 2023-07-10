from flask import Flask, request, jsonify
import datetime
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

app = Flask(__name__)

@app.route('/stock-data', methods=['GET'])
def get_stock_data():
    ticker = request.args.get('ticker')
    date_string = request.args.get('date')

    # parsing date string to datetime type
    date = datetime.datetime.strptime(date_string, '%d/%m/%Y').date()
    start_date = datetime.datetime(date.year, date.month, date.day)
    end_date = datetime.datetime.now().date()

    ts = TimeSeries(key=api_key, output_format="pandas")
    data_daily, meta_data = ts.get_daily_adjusted(symbol=ticker, outputsize='full')

    data_daily.index = pd.to_datetime(data_daily.index)

    date_filter = data_daily[(data_daily.index > pd.Timestamp(start_date)) & (data_daily.index <= pd.Timestamp(end_date))]
    date_filter = date_filter.sort_index(ascending=True)

    # converting cleaned dataframe to json format
    date_filter_json = date_filter.reset_index().to_json(orient='records')

    return jsonify(date_filter_json)

if __name__ == '__main__':
    app.run()
