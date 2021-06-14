# Long Short Term Memory LSTM to predict the closing stock prices

# Import the libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas_datareader as pdr
import pandas as pd
import datetime as dt

# import numpy as np
# import math

# from sklearn.preprocessing import MinMaxScaler
# from keras.models import Sequential
# from keras.layers import Dense, LSTM


# Yesterday because today's market might not be closed.
today = dt.datetime.now()
yesterday = (today - dt.timedelta(days=1)).strftime('%Y-%m-%d')

# df = pdr.DataReader('AAPL', data_source='yahoo', start='2015-01-01', end=yesterday)
# print(df.head())

#
# print(df.head())
# print('rows, columns', df.shape)
# print(df[df.index > today - dt.timedelta(days=121)].describe())


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, "style.css"],
                # Mobile responsive
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(
            html.H1('Stock Price Trend',
                    className='text-center text-primary',
                    style={"margin":"5%"}),
        width=12),
    align="center"),

    dbc.Row([
        dbc.Col(
            html.H5("Stock Symbol",
                        style={"margin":"3%", "text-align":"center"}),
            width=3),

        dbc.Col(
            dbc.Input(
                id="input1",
                type="text",
                placeholder="",
                debounce=True,
                value="^GDAXI",
                bs_size="sm"),
            width=4),

        dbc.Col(
            dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=dt.date(2000,1,1),
            max_date_allowed=yesterday,
            initial_visible_month=yesterday,
            end_date=yesterday,
            className="date_range"),
        width={"size":4, "offset":1}),
        # html.Div(id='output-container-date-picker-range')
    ], justify="left"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="line-fig")
        ])
    ])

])


# Callback section: connecting the components
# ************************************************************************
# Line chart - Single
@app.callback(
    Output('line-fig', 'figure'),
    [Input('input1', 'value'),
     Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_graph(stock_slctd, start_date, end_date ):
    print(stock_slctd)
    print(type(stock_slctd))
    # Get the stock quote
    # TODO: Users input 1.stock_symbol 2.start/end dates
    df = pdr.DataReader(stock_slctd, data_source='yahoo', start=start_date, end=end_date)
    print(df.head())
    figln = px.line(df, y='Close')
    return figln


if __name__ == "__main__":
    app.run_server(debug=True, port=8000)
