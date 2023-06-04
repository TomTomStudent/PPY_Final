# apikey = HO00WY71XPUJO3ND
import csv
from sqlite3 import Timestamp
from tkinter import *
import tkinter
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# initialize  GUI
root = Tk()
root.title('Stocks babeeeeeeee')
root.geometry("600x600")

fig, ax = plt.subplots(figsize=(5, 5), dpi=100)

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

timestamps = []
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        if row:
            timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            timestamps.append(timestamp)
variables = []

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=BOTH, expand=True)


def order_num(argument):
    switcher = {
        "Open": 1,
        "High": 2,
        "Low": 3,
        "Close": 4,
        "Volume": 5,
    }
    return switcher.get(argument, 1)


def update_graph():
    timestamps.clear()
    variables.clear()

    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                variable = float(row[order_num(var_list_val.get())])
                timestamps.append(timestamp)
                variables.append(variable)
    ax.clear()
    ax.plot(timestamps, variables)

    ax.set_xlabel('Timestamp')
    ax.set_ylabel(var_list_val.get())
    ax.set_title(var_list_val.get())
    plt.xticks(rotation=45)

    canvas.draw()


var_list = ["Open", "High", "Low", "Close", "Volume"]
time_list = [str(timestamp) for timestamp in timestamps]

var_list_val = tkinter.StringVar(root)
var_list_val.set("Select value")
var_time_list = tkinter.StringVar(root)
var_time_list.set("Select date")

q1_menu = tkinter.OptionMenu(root, var_list_val, *var_list)
q2_menu = tkinter.OptionMenu(root, var_time_list, *time_list)

q1_menu.pack(side="right")
q2_menu.pack(side="right")


def go():
    update_graph()
    print("Option 1: {}".format(var_list_val.get()))
    print("Option 2: {}".format(var_time_list.get()))


go_button = tkinter.Button(
    root, text='GO->>', command=go)

go_button.pack(side="right")

update_graph()


def on_closing():
    plt.close(fig)
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
