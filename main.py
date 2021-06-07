import streamlit as st
import pandas_datareader as web
import requests
import pandas as pd
from PIL import Image
from datetime import datetime
from plotly import graph_objs as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import yfinance as yf

st.set_page_config(layout="wide")

# Adding a Title and image to the Webapp
st.write("""
# Stock Market Web Application 
**Visually display data on a stock and a machine learning model to predict future prices**
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
    df = web.DataReader(str(symbol), data_source='yahoo', start=start, end=end)

    return df


# Creating a function to select on sidebar which type of information they would like to view

# Getting User input
start, end, symbol, data_type = user_input()

# writing element #2 of the sidebar
st.sidebar.write("""
### 2. Stock Prediction 
Select a stock you would like the model to forecast using the box above, use the slider to select how many years ahead you would like the model to predict.
""")
# About section of the sidebar
st.sidebar.title("About")
st.sidebar.write(f"""
**This project is made by Aashir Meeran - University of Toronto Engineering Science Student**
""")

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

# FORECASTING MACHINE LEARNING COMPONENT OF THE WEB APPLICATION

st.title("Stock Prediction Component")
st.write(f"""### Selected Company: {company_name}""")

# Defining a start and end date to download data
start = '2015-01-01'
end = str(datetime.date(datetime.now()))

n_years = st.slider("Years of prediction", 1, 4)
period = n_years * 365


# downloading the data - @st.cache caches the loaded data do it stores the data in cache.
@st.cache
def load_data(symbol):
    data = yf.download(symbol, start, end)
    data.reset_index(inplace=True)
    return data


data2 = load_data(symbol)
st.subheader("Raw Data")


# PLOTTING THE RAW DATA

def graph_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data2['Date'], y=data2['Open'], name='Stock Open'))
    fig.add_trace(go.Scatter(x=data2['Date'], y=data2['Close'], name='Stock Close'))

    fig.layout.update(
        xaxis_rangeslider_visible=True)

    fig.update_layout(
        autosize=True
    )

    st.plotly_chart(fig)


graph_raw_data()

# Forecasting using FBPROPHET

dataframe_train = data2[['Date', 'Close']]
dataframe_train = dataframe_train.rename(columns={"Date": "ds", "Close": "y"})

model = Prophet()
model.fit(dataframe_train)
future = model.make_future_dataframe(periods=period)

# Predicting
forecast = model.predict(future)

# Plotting
st.title('Predicted Data')

# Plotting the forecasted data

fig1 = plot_plotly(model, forecast)
st.plotly_chart(fig1)

st.write(forecast)

st.subheader('Predicted Data Components')
fig2 = model.plot_components(forecast)
st.write(fig2)
