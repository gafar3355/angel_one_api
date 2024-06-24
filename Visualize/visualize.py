import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

df=pd.read_csv(r"C:\Users\Dell 1\OneDrive\Desktop\angel_api\candlestick_data\axis_bank_candlestick_data.csv")

df['exchange_timestamp'] = pd.to_datetime(df['exchange_timestamp'])


exchange_rate = 0.01
df['open'] *= exchange_rate
df['high'] *= exchange_rate
df['low'] *= exchange_rate
df['close'] *= exchange_rate


fig= go.Figure(data=[go.Candlestick(x=df['exchange_timestamp'],
                                    open=df['open'],
                                    high=df['high'],
                                    low=df['low'],
                                    close=df['close'])])

fig.update_layout(title='Axis Bank Candlestick Chart',
                  xaxis_title='Time',
                  yaxis_title='Price',
                  yaxis=dict(tickprefix="₹"))

fig.show()

