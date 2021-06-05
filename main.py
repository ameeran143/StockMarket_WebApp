import streamlit as st
import pandas_datareader as web
import requests
import pandas as pd
from PIL import Image
from datetime import datetime

st.set_page_config(layout="wide")

# Adding a Title and image to the Webapp
st.write("""
# Stock Market Web Application 
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
    data_type = st.sidebar.selectbox("Data to Display", ["Volume", "Opening Price", "Closing Price"])
    return start_date, end_date, stock_symbol, data_type


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


# Creating a function to select on sidebar which type of information they would like to view


# Getting User input
start, end, symbol, data_type = user_input()

if data_type == "Closing Price":
    data = "Close"
elif data_type == "Opening Price":
    data = "Open"
else:
    data = "Volume"

# Getting the Data
df = get_data(symbol, start, end)

# Getting the Company name
company_name = get_company_name(symbol.upper())

# Displaying information
st.header(company_name + " " + data_type + "\n")
st.line_chart(df[data])

# Displaying Statistics about the Data
st.header("Analysis of Data")
st.write(df.describe())
