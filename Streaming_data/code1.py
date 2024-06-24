import os
import csv
import pandas as pd
import time
import concurrent.futures
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from SmartApi import SmartConnect
from pyotp import TOTP
from datetime import datetime


key_path = r"C:\\Users\Dell 1\\OneDrive\\Documents\\Bills"
os.chdir(key_path)

key_secret = open("key.txt","r").read().split()

obj=SmartConnect(api_key=key_secret[0])
data = obj.generateSession(key_secret[2],key_secret[3],TOTP(key_secret[4]).now())
feed_token = obj.getfeedToken()

sws = SmartWebSocketV2(data["data"]["jwtToken"], key_secret[0], key_secret[2], feed_token)


correlation_id = "stream_2"   #unique stream id
action = 1     #1 subscribe, 0 unsubscribe
mode = 2       #2 - QOUTE & 3 - SNAPQOUTE

token_list = [
    {"exchangeType": 1, "tokens": ["3045"]}, # SBIN
    {"exchangeType": 1, "tokens": ["4963"]}, # ICICI
    {"exchangeType": 1, "tokens": ["1333"]}, # HDFC
    {"exchangeType": 1, "tokens": ["1023"]}, # FEDERAL BANK
    {"exchangeType": 1, "tokens": ["5900"]}, # AXIS BANK
]

local_path = r"C:\Users\Dell 1\OneDrive\Desktop\angel_api"


def create_candle(token, file_name):
    while True:
        try:
            time.sleep(60)  # Sleep for 60 seconds before processing next candle
            df = pd.read_csv(f"{local_path}/data/{file_name}_market_data.csv")
            df["exchange_timestamp"] = pd.to_datetime(df["exchange_timestamp"])
            df.set_index("exchange_timestamp", inplace=True)

            candle = df.resample("1min").agg({"last_traded_price": ["first", "max", "min", "last"]})

            candle.dropna(inplace=True)
            candle.columns = ['open', 'high', 'low', 'close']
            candle.to_csv(f"{local_path}/candlestick_data/{file_name}_candlestick_data.csv")

            
        except Exception as e:
            print("Error")

def create_all_candles():
    token_file_mapping = {
        "3045": "sbin",
        "4963": "icici",
        "1333": "hdfc",
        "1023": "federal_bank",
        "5900": "axis_bank"
    }
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for token, file_name in token_file_mapping.items():
            executor.submit(create_candle, token, file_name)


def appen_data_into_csv(file_name, message):
    with open(f"{local_path}/data/{file_name}.csv", "a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=message.keys())

        csv_file.seek(0, 2)
        if csv_file.tell() == 0:
            writer.writeheader()

        writer.writerow(message)


def on_data(wsapp, message):
    message["exchange_timestamp"] = datetime.fromtimestamp(message["exchange_timestamp"] /1000.0)

    if message["token"] == "3045":
        appen_data_into_csv("sbin_market_data", message)

    elif message["token"] == "4963":
        appen_data_into_csv("icici_market_data", message)

    elif message["token"] == "1333":
        appen_data_into_csv("hdfc_market_data", message)

    elif message["token"] == "1023":
        appen_data_into_csv("federal_bank_market_data", message)

    elif message["token"] == "5900":
        appen_data_into_csv("axis_bank_market_data", message)


def on_open(wsapp):
    print("on open")
    sws.subscribe(correlation_id, mode, token_list)


def on_error(wsapp, error):
    print(error)



def start_websocket():
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error

    sws.connect()


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(start_websocket)
    executor.submit(create_all_candles)
