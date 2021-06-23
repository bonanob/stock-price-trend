# Project 6: Stock Price Trend

This web application shows a candlestick stock price chart and volume chart(bar) below. Users can search with stock(ticker) symbols, and set date range to focus on specific time period. 

**How to run the project locally:**

1. Create a virtual environment
    - Mac: **`python3 -m venv venv`**
    - Windows: **`python -m venv venv`**
2. Activate your environment
    - Mac: **`source ./env/bin/activate`**
    - Windows: **`.\env\Scripts\activate`**
3. Install dependancies: **`pip install -r requirements.txt`**
4. Run the file **`app.py`**

**What I've learned:**

- Using API(yfinance) to pull data.
- Basics of Pandas

- Plotly graphic library
- Plotly dash framework

**Objective:** 

Create a web application to display stock charts.

**Features:**

- Search by stock symbol
- Interactive plotly graph(zoom, hover for values, compare values, etc.)
- Moving avg, volume chart
- Range buttons(1m, 6m, 1y, 5y)
- Range field with calendar date picker
- error pop-up when no search result

**Future Improvements:**

- Prediction model
- Auto search suggestion
- Comparison with sector / market
- Auxiliary indicators
- Market / Company Info
