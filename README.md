# Implementation of "Flask on Heroku" DI project.

The project asks the user for stock ticker input and a selection of price types
and supplies a graph of that stock and those price types for the past two years.

If an invalid ticker is given the user is re-prompted for a new one and given
a basic error message.

## index.html

Page for entering stock ticker together with four checkboxes for price types, one
each for open, close, and adjusted open, adjusted close.

## pricegraph.html

Page for rendering the plot specified by the user.

## app.py

The app takes the stock ticker and requests the past two years of data from the
QUANDL Wiki data set using a hidden QUANDL API key. The data is then processed 
into a dataframe by pandas, which is then read into a graph by Bokeh and the 
result is fed to pricegraph.html for rendering. The price type inputs specified
by the user select an appropriate number of graphs from the data.

### See below for original README.md:

# Flask on Heroku

This project is intended to help you tie together some important concepts and
technologies from the 12-day course, including Git, Flask, JSON, Pandas,
Requests, Heroku, and Bokeh for visualization.

The repository contains a basic template for a Flask configuration that will
work on Heroku.

A [finished example](https://lemurian.herokuapp.com) that demonstrates some basic functionality.

## Step 1: Setup and deploy
- Git clone the existing template repository.
- `Procfile`, `requirements.txt`, `conda-requirements.txt`, and `runtime.txt`
  contain some default settings.
- There is some boilerplate HTML in `templates/`
- Create Heroku application with `heroku create <app_name>` or leave blank to
  auto-generate a name.
- (Suggested) Use the [conda buildpack](https://github.com/kennethreitz/conda-buildpack).
  If you choose not to, put all requirements into `requirements.txt`

  `heroku config:add BUILDPACK_URL=https://github.com/kennethreitz/conda-buildpack.git`
- *Question*: What are the pros and cons of using conda vs. pip?
- Deploy to Heroku: `git push heroku master`
- You should be able to see your site at `https://<app_name>.herokuapp.com`
- A useful reference is the Heroku [quickstart guide](https://devcenter.heroku.com/articles/getting-started-with-python-o).

## Step 2: Get data from API and put it in pandas
- Use the `requests` library to grab some data from a public API. This will
  often be in JSON format, in which case `simplejson` will be useful.
- Build in some interactivity by having the user submit a form which determines which data is requested.
- Create a `pandas` dataframe with the data.

## Step 3: Use Bokeh to plot pandas data
- Create a Bokeh plot from the dataframe.
- Consult the Bokeh [documentation](http://bokeh.pydata.org/en/latest/docs/user_guide/embed.html)
  and [examples](https://github.com/bokeh/bokeh/tree/master/examples/embed).
- Make the plot visible on your website through embedded HTML or other methods - this is where Flask comes in to manage the interactivity and display the desired content.
- Some good references for Flask: [This article](https://realpython.com/blog/python/python-web-applications-with-flask-part-i/), especially the links in "Starting off", and [this tutorial](https://github.com/bev-a-tron/MyFlaskTutorial).
