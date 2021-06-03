import streamlit as st
import pandas_datareader as web
import requests
import pandas as pd
from PIL import Image
from datetime import datetime

# Adding a Title and image to the Webapp
st.write("""
# Stock Market WebApp 
**Visually display data on a stock and a machine learning model to predict future prices.**
""")

pic = Image.open("StockMarketWebapp.png")
st.image(pic, use_column_width=True)

# Creating a Sidebar
st.sidebar.write("""
# Table of Content
### 1. Information Display - Select Options
""")


# Creating a function to get user input
def user_input():
    start_date = st.sidebar.text_input("Start Date", '2000-01-01')
    end_date = st.sidebar.text_input("End Date", datetime.date(datetime.now()))
    stock_symbol = st.sidebar.text_input("Stock Symbol", 'AMZN')
    return start_date, end_date, stock_symbol


# Creating a function to get Company name
def get_company_name(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']


# Creating a function to get the company data and time frame
def get_data(symbol, start, end):
    # Load the Data
    df = web.DataReader(symbol, data_source='yahoo', start=start, end=end)

    return df


# Getting User input
start, end, symbol = user_input()

# Getting the Data
df = get_data(symbol, start, end)

# Getting the Company name
company_name = get_company_name(symbol.upper())

# Dsiplaying information
st.header(company_name + " Close Price\n")
st.line_chart(df['Close'])
