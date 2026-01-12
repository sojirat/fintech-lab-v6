import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title("📈 Real-Time Stock Price Viewer")

stock = st.text_input("Enter Stock Ticker", "AAPL")
if stock:
    data = yf.download(stock, start="2022-01-01")
    st.write(f"Showing closing prices for {stock}")
    st.line_chart(data['Close'])

    st.write("Raw data:")
    st.dataframe(data.tail())