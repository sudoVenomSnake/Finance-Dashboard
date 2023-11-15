import streamlit as st
import plotly.express as px
import yfinance as yf

st.set_page_config(layout = "wide", page_title = "Dashboard")

st.title("Finance Dashboard")

col1, col2 = st.columns(2)
with col1:
    st.subheader("NIFTY 50")
    st.plotly_chart(px.line(yf.download(tickers = "^NSEI"), y = "Close"), use_container_width = True)
with col2:
    st.subheader("India VIX")
    st.plotly_chart(px.line(yf.download(tickers = "^INDIAVIX", interval = "1m", period = "1d"), y = "Close"), use_container_width = True)