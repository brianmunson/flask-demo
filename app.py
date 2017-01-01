from flask import Flask, render_template, request, redirect
import requests
import os
import pandas as pd
import datetime
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from dotenv import find_dotenv, load_dotenv

# getting QUANDL credentials from environmental variables
load_dotenv(find_dotenv())
quandl_key = os.environ.get("QUANDL")

###### for loading secret API key. Now unecessary b/c of environmental variables.
# File should be a single line containing key, in same directory as this program.
# Open file, turn into string which excludes \n at the end, close the file.
# Return is a string. Mileston app has better version of this that requires
# only one key_file for every possible API key.
#
# def openAPI_Key(key_file):
#     f = open(key_file, 'r')
#     api_key = f.read().rstrip()
#     f.close()
#     return(api_key)


###### for obtaining the appropriate url, fetching data, and creating pandas
# dataframe for the data
# https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker=<your_codes>&date=<your_date>&qopts.columns=<your_columns>&api_key=xd8JeTNonwzxjm1dzssa

def get_quandl_df(ticker, api_key):
    ticker = ticker.upper()
    today = datetime.datetime.now()
    today_str = str(today.year)+str(today.month)+str(today.day)
    back_then = today - datetime.timedelta(days = 730)
    back_then_str = str(back_then.year)+str(back_then.month)+str(back_then.day)

    quandl_url = "https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?" + \
    "date.gte=" + back_then_str + "&date.lt=" + today_str + "&ticker=" + ticker + \
    "&api_key=" + api_key

    r = requests.get(quandl_url)
    if r.status_code < 400 :
        # this is not the result of an invalid ticker: i can successfully
        # retrieve an object r from invalid ticker, it gives empty 'datatable'
        data_dict = r.json()['datatable']
        columns = [item['name'] for item in data_dict['columns']]
        df = pd.DataFrame(data_dict['data'], columns = columns)
        df = df.set_index(pd.DatetimeIndex(df['date']))
        # sets appropriate index for plotting later on

        # if no error, get the data
        # data_dict = r.json()['datatable']
        # data_dict['columns'] is a list of dicts
        # want the columns corresponding to the key-value pairs
        # 'name' : 'ticker', 'name' : 'date', 'name' : 'open', 'name' : 'close',
        # 'name' : 'adj_open', 'name' : 'adj_close'. get the indices of these
        # use data_dict['data'] (a list of lists, each list corresponds to the
        # columns of data_dict['columns'])
        # df = pd.DataFrame(data_dict['data'], columns = data_dict['columns'])
    else:
        print("Stock ticker invalid or not in the database.")
    return(df)

###### for bokeh to create appropriate plot of the data frame.
# arguments are a dataframe, price_type, and ticker

def make_plot(df, prices, ticker):
    colors = ["red", "blue", "green", "yellow"]
    prices = pd.Series(prices)
    # force to pandas series, which is always iterable even if length 1, and
    # allows the enumerate method
    p = figure(x_axis_type = "datetime", title = ticker)
    p.grid.grid_line_alpha = 0.3
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Price"
    for price in enumerate(prices) :
        p.line(df.index, df[price[1]], color = colors[price[0]])
    # p.line(df.index, df['high'], color = "pink") # for help debugging
    script, div = components(p)
    return(script, div)
    # current plot only seems to go back 12 months. is this an issue of scaling
    # with bookeh? the data is all there for 24 months.

app = Flask(__name__)

app.vars = {}
# key_file = "API_Key" # for old way of getting API key.
app.vars['api key'] = quandl_key

@app.route('/')
def main():
    return(redirect('/index'))

@app.route('/index', methods = ['GET', 'POST'])
def index():
    return(render_template('index.html', msg = ''))

@app.route('/pricegraph', methods = ['GET', 'POST'])
def pricegraph():
     if request.method == 'POST':
         ticker = request.form["ticker"]
         ticker = ticker.upper()
         prices = request.form.getlist("price_type")
         df = get_quandl_df(ticker, app.vars['api key'])
        #  script, div = make_plot(df, prices, ticker)
        #  return(render_template('pricegraph.html', script = script, div = div, ticker = ticker))
         if df.empty:
             return(render_template('index.html', msg = "Invalid ticker"))
         else:
             script, div = make_plot(df, prices, ticker)
             return(render_template('pricegraph.html', script = script, div = div, ticker = ticker))
     else:
         return(render_template('index.html', msg = ''))


if __name__ == '__main__':
    # port=int(os.environ.get("PORT", 5000)) # run locally
    # app.run(port=port, host='0.0.0.0', debug=True) # run locally
    app.run(port=33507) # run on Heroku
