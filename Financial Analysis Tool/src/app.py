import datetime
import pandas as pd
import streamlit as st
import yfinance as yf
from utils import convert_to_csv, get_stock_data, get_stocks,compare_with_chatgpt

st.header('Financial Analysis Tool', divider='red')


stock = st.selectbox(key=0,label='Selct stock:',options=get_stocks(),index=None)
compare = st.checkbox("Compare two stocks")
compare_stock=None
if compare:
    compare_stock = st.selectbox(key=1,label='Select the stock you want to compare ',options=get_stocks(),index=None)


today = datetime.datetime.now()
next_day = today+datetime.timedelta(days=1)
jan_1 = datetime.date(today.year-20, 1, 1)
dec_31 = datetime.date(today.year, 12, 31)

date_range = st.date_input(
    "Enter a date range",
    (today, next_day),
    jan_1,
    dec_31,
    format="MM.DD.YYYY"
)


chart_selections = {
 "Line Chart":st.line_chart,
 "Bar Chart":st.bar_chart
}

COLUMNS = ("Open","High","Low","Close","Adj Close","Volume")

if len(date_range)==2:
    if stock and compare_stock:
        stock_data = get_stock_data(stock,date_range[0],date_range[1])
        compare_stock_data = get_stock_data(compare_stock,date_range[0],date_range[1])
        st.title("Fetched data")
        col1, col2 = st.columns(2)
        with col1:
          st.write(f"You are searching for {stock} stock from {date_range[0]} to {date_range[1]} time period.")
          st.write(stock_data)
          if not stock_data.empty:
            chart_option =  st.selectbox(key=3,label='Select chart element',options=["Line Chart","Bar Chart"])
            plot_option =  st.selectbox(key=8,label='Select the column you want to plot',options=COLUMNS)
            if chart_option:
                chart_selections[chart_option](stock_data[plot_option])
        with col2:
          st.write(f"You are searching for {compare_stock} stock from {date_range[0]} to {date_range[1]} time period.")
          st.write(compare_stock_data)
          if not compare_stock_data.empty:
            compare_chart_option =  st.selectbox(key=4,label='Select chart element',options=["Line Chart","Bar Chart"])
            plot_option =  st.selectbox(key=9,label='Select the column you want to plot',options=COLUMNS)
            if compare_chart_option:
                chart_selections[compare_chart_option](compare_stock_data[plot_option])
        if st.button("Compare stocks",disabled=stock_data.empty,type="primary"):
            comparison = compare_with_chatgpt(stock_data,compare_stock_data)
            if comparison:
                st.title(f"Comparisong between {stock} and {compare_stock}")
                st.write(comparison)

    if not compare and stock:
        stock_data = get_stock_data(stock,date_range[0],date_range[1])
        st.download_button(
        "Download stocks to csv",
        convert_to_csv(stock_data),
        f"{stock} stocks.csv",
        "text/excel",
        key='download-to-csv',
        disabled=stock_data.empty
        )
        st.title("Fetched data")
        st.write(f"You are searching for {stock} stock from {date_range[0]} to {date_range[1]} time period.")
        st.write("Data operations")
        if not stock_data.empty:
            col1, col2, col3 = st.columns([0.5,0.5,0.4])
            with col1:
                operatin_option =  st.selectbox(key=5,label="Operation",options=["Mean","Max","Min","Count"])
            with col2:
                column_option =  st.selectbox(key=6,label="Column",options=COLUMNS)
            with col3:
                OPERATIONS ={
                    "Mean":stock_data[column_option].mean,
                    "Max":stock_data[column_option].max,
                    "Min":stock_data[column_option].min,
                    "Count":stock_data[column_option].count
                }
                st.write("Output")
                st.write(round(OPERATIONS[operatin_option](),2))
        st.write(stock_data)
        if not stock_data.empty:
            chart_option =  st.selectbox(key=7,label='Select chart element',options=["Line Chart","Bar Chart"])
            plot_option =  st.selectbox(key=2,label='Select the column you want to plot',options=COLUMNS)
            if chart_option:
                chart_selections[chart_option](stock_data[plot_option])
