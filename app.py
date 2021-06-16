# TODO: Long Short Term Memory LSTM to predict the closing stock prices

# Import the libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import pandas as pd
import datetime as dt
import yfinance as yf

# import numpy as np
# import math

# from sklearn.preprocessing import MinMaxScaler
# from keras.models import Sequential
# from keras.layers import Dense, LSTM


# Yesterday because today's market might not be closed.
today = dt.datetime.now()
yesterday = (today - dt.timedelta(days=1)).strftime("%Y-%m-%d")


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, "style.css"],
                # Mobile responsive
                meta_tags=[{"name": "viewport",
                            "content": "width=device-width, initial-scale=1.0"}]
                )

app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(
            html.H1("Stock Price Trend",
                    className="text-center text-primary",
                    style={"margin": "3%"}),
            width=12),
        align="center"),

    dbc.Row([
        dbc.Col(
            html.H5("Stock Symbol",
                    style={"margin": "3%", "text-align": "center"}),
            width=3),

        dbc.Col(
            dbc.Input(
                id="symbol",
                type="text",
                placeholder="",
                bs_size="sm",
                debounce=True),
            width=4),

        dbc.Col(
            dcc.DatePickerRange(
                id="date_range",
                display_format='DD-MM-YYYY',
                min_date_allowed=dt.date(2000, 1, 1),
                max_date_allowed=yesterday,
                initial_visible_month=yesterday,
                start_date=dt.date(2021, 1, 1),
                end_date=yesterday),
            width={"size": 4, "offset": 1}),
    ], justify="left", style={"margin":"5px 0px"}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="line-fig")
        ])
    ])

])


# Callback section: connecting the components
# ************************************************************************
=@app.callback(
    Output("line-fig", "figure"),
    [Input("symbol", "value"),
     Input("date_range", "start_date"),
     Input("date_range", "end_date")]
)
def update_graph(symbol, start_date, end_date):
    # Set initial ticker symbol
    if symbol is None:
        yf_symbol = yf.Ticker("^GDAXI")
    else:
        yf_symbol = yf.Ticker(symbol)


    # .info["shortName"] for the name of the company
    info = yf_symbol.info

    # .history for the historical data
    hist = yf_symbol.history(start=start_date, end=end_date)

    # Moving average
    hist["ma_5"] = hist["Close"].rolling(window=5, min_periods=0).mean()
    hist["ma_20"] = hist["Close"].rolling(window=20, min_periods=0).mean()
    hist["ma_60"] = hist["Close"].rolling(window=60, min_periods=0).mean()
    hist["ma_120"] = hist["Close"].rolling(window=120, min_periods=0).mean()

    # To make two plots that share x axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_width=[0.2, 0.7])

    # .add_trace for adding plots to existing plot
    fig.add_trace(
        go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'],
                       name="OHLC"), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=hist["ma_5"], marker_color="purple", name="MA5"), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=hist["ma_20"], marker_color="orange", name="MA20"), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=hist["ma_60"], marker_color="cyan", name="MA60"), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=hist["ma_120"], marker_color="pink", name="MA120"), row=1, col=1)
    fig.add_trace(go.Bar(x=hist.index, y=hist["Volume"], marker_color="black", showlegend=False), row=2, col=1)

    # plot styling
    fig.update_layout(
        margin=dict(l=80, r=80, t=80, b=80),
        title={'text': info["shortName"], 'font': {'size': 16}, 'x': 0.08, 'y': 0.93, 'xanchor': 'left'},
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Price',
            titlefont_size=14,
            tickfont_size=12
        ),
        autosize=False,
        height=800,
    )

    # Remove rangeslider
    fig.update(layout_xaxis_rangeslider_visible=False)


    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8000)

    # token = "Tpk_b880885bcfdb4be2aa9eb43c6455eabb"
    #
    # api_url = f"https://sandbox.iexapis.com/stable/stock/aapl/quote/?token={token}"
    #
    # data = requests.get(api_url).json()
    # print(data)
    #
    # api_url1 = f"https://sandbox.iexapis.com/stable/search/apple/?token={token}"
    # data1 = requests.get(api_url1).json()
    # print(data1)

    # df = pd.read_json(data[0])
    # print(df)
