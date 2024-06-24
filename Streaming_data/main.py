from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from SmartApi import SmartConnect
import os
from pyotp import TOTP
import csv
import datetime

key_path = r"C:\\Users\Dell 1\\OneDrive\\Documents\\Bills"
os.chdir(key_path)
key_secret = open("key.txt","r").read().split()

obj = SmartConnect(api_key=key_secret[0])
data = obj.generateSession(key_secret[2], key_secret[3], TOTP(key_secret[4]).now())
feed_token = obj.getfeedToken()

sws = SmartWebSocketV2(data["data"]["jwtToken"], key_secret[0], key_secret[2], feed_token)


correlation_id = "stream_1"
action = 1  
mode = 3    

token_list = [
    {"exchangeType": 1 , "tokens": ["3045"]},  #SBIN
    {"exchangeType": 1, "tokens": ["4963"]},   #ICICIBANK
    {"exchangeType": 1, "tokens": ["1333"]},   #HDFC 
    {"exchangeType": 1, "tokens": ["1023"]},   #FEDERALBNK 
    {"exchangeType": 1, "tokens": ["5900"]}    #AXISBANK 
]


def on_data(wsapp, message):
    message["exchange_timestamp"] = datetime.datetime.fromtimestamp(message.get("exchange_timestamp", 0) / 1000).strftime('%Y-%m-%d %H:%M:%S')

    print("Ticks: {}".format(message) + "\n")

    # Appending the received data to the CSV file
    with open(r'C:\Users\Dell 1\OneDrive\Desktop\angel_api\testfy.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=message.keys())
        if file.tell() == 0:  
            writer.writeheader()
        writer.writerow(message)
    

def on_open(wsapp):
    print("on open")
    sws.subscribe(correlation_id, mode, token_list)


def on_error(wsapp, error):
    print(error)


sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error

sws.connect()


