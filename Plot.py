import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
import pandas as pd

from tickers import yahoo_finance_tickers

st.set_page_config(layout = "wide", page_title = "Dashboard")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# @st.cache_data
def get_nsei_df():
    x1 = yf.download(tickers = "^NSEI", interval = "1m", period = "1d")
    x2 = yf.download(tickers = "^INDIAVIX", interval = "1m", period = "1d")
    return pd.DataFrame({"Date & Time" : x1.index, "NIFTY" : x1["Close"].to_list(), "INDIA VIX" : x2["Close"].to_list()})

st.title("Finance Dashboard")

company = st.selectbox(label = "Please select a company indexed in NIFTY50 -", options = yahoo_finance_tickers.keys())

if company:
    df = yf.download(tickers = yahoo_finance_tickers[company], interval = "1d", period = "1y")
    moving_average = st.slider(label = "Moving Average -", min_value = 0, max_value = 100, value = 0)
    fig = make_subplots()
    fig.add_trace(
        go.Scatter(x = df.index, y = df["Close"], name = company)
    )
    if moving_average > 0:
        fig.add_trace(
            go.Scatter(x = df.index, y = df["Close"].rolling(window = moving_average).mean(), name = str(moving_average)+ " MA")
        )
        fig.update_yaxes(title_text = company)
        fig.update_yaxes(title_text = str(moving_average) + " MA")
    fig.update_xaxes(title_text = "Date")
    fig.update_layout(
        title_text = company
    )
    st.plotly_chart(fig, use_container_width = True)

df = get_nsei_df()
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Scatter(x = df["Date & Time"], y = df["NIFTY"], name = "NIFTY"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x = df["Date & Time"], y = df["INDIA VIX"], name = "INDIA VIX"),
    secondary_y = True,
)

fig.update_layout(
    title_text = "Nifty With India VIX"
)

fig.update_xaxes(title_text = "Date & Time")
fig.update_yaxes(title_text = "NIFTY", secondary_y = False)
fig.update_yaxes(title_text = "INDIA VIX", secondary_y = True)
st.plotly_chart(fig, use_container_width = True)
