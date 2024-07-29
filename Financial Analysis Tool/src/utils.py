import os
import yfinance as yf
from openai import OpenAI
from pytickersymbols import PyTickerSymbols


stock_data = PyTickerSymbols()
client = OpenAI(api_key=os.environ.get("API_KEY"),project=os.environ.get("PROJECT"))

def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def get_stocks():
    return [ticker.get("symbol")for ticker in stock_data.get_all_stocks()]

def convert_to_csv(df):
    return  df.to_csv(index=False).encode('utf-8')

def compare_with_chatgpt(stock0,stock1):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a financial assistant that will retrieve two tables of financial market data and will summarize the comparative performance in text, in full detail with highlights for each stock and also a conclusion with a markdown output. BE VERY STRICT ON YOUR OUTPUT"},
                {"role": "user", "content": f"Compare the following stocks, {stock0} and {stock1}. Give a brief explanation."}
                ]
        )
    return response.choices[0].message.content
