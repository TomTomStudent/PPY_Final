# apikey = HO00WY71XPUJO3ND
import csv
import requests

# api grabbing the data about the stock
CSV_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol=IBM&interval=60min&slice=year1month1&apikey=HO00WY71XPUJO3ND'

with requests.Session() as s:
    download = s.get(CSV_URL)

    with open('data.csv', 'w') as f:
        f.write(download.text)

# currently data.csv has the data from 30 most recent days of IBM stock data taken every hour
# info for how the data is saved in the csv file:
# Open: The opening price is the price at which a particular stock starts trading at the beginning of a trading session or market day.
# High: The high price represents the highest price level that the stock reached during the trading session or market day.
# Low: The low price represents the lowest price level that the stock reached during the trading session or market day.
# Close: The closing price is the final price at which the stock traded at the end of the trading session or market day.
# Volume: Volume refers to the total number of shares traded for a particular stock during a given trading session or market day. It indicates the level of activity and liquidity in the stock market for that specific stock.

with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            print(row)
