import os
import psycopg2
import csv
import concurrent.futures
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from SmartApi import SmartConnect
from pyotp import TOTP
import datetime                                            
import concurrent.futures
                                               

key_path = r"C:\\Users\Dell 1\\OneDrive\\Documents\\Bills"
os.chdir(key_path)


key_secret = open("key.txt","r").read().split()


obj = SmartConnect(api_key=key_secret[0])
data = obj.generateSession(key_secret[2], key_secret[3], TOTP(key_secret[4]).now())
feed_token = obj.getfeedToken()


sws = SmartWebSocketV2(data["data"]["jwtToken"], key_secret[0], key_secret[2], feed_token)


correlation_id = "stream_1" 

action = 1  # 1 subscribe, 0 unsubscribe
mode = 3    # 1 for LTP, 2 for Quote and 2 for SnapQuote
token_list = [
    {"exchangeType": 1 , "tokens": ["3045"]},  #SBIN
    {"exchangeType": 1, "tokens": ["4963"]},   #ICICIBANK
    {"exchangeType": 1, "tokens": ["1333"]},   #HDFC 
    {"exchangeType": 1, "tokens": ["1023"]},   #FEDERALBNK 
    {"exchangeType": 1, "tokens": ["5900"]}    #AXISBANK 
]

# conn = psycopg2.connect(
#     dbname="stock_market",
#     user="postgres",
#     password="DataRig@123",
#     host="localhost",
#     port="5432"
# )

# cursor = conn.cursor()

def flatten_data(data):
    flat_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            flat_data.update({f"{key}_{subkey}": subvalue for subkey, subvalue in value.items()})
        else:
            flat_data[key] = value
    return flat_data


# Callback function to handle incoming data
def on_data(wsapp, message):
    # try:
    #     updated_message = message.copy()  # Create a copy of the original message

    #     # Convert last_traded_timestamp to real-time
    #     last_traded_timestamp = message["exchange_timestamp"] / 1000
    #     real_time = datetime.datetime.fromtimestamp(last_traded_timestamp)
    #     formatted_time = real_time.strftime('%Y-%m-%d %H:%M:%S')

    #     # Update last_traded_timestamp in the copied message
    #     updated_message["exchange_timestamp"] = formatted_time

    #     insert_query = '''INSERT INTO market_data(
    #     token,
    #     sequence_number,
    #     exchange_timestamp,
    #     last_traded_price,
    #     last_traded_quantity,
    #     average_traded_price,
    #     volume_trade_for_the_day,
    #     total_buy_quantity,
    #     total_sell_quantity,
    #     open_price_of_the_day,
    #     high_price_of_the_day,
    #     low_price_of_the_day,
    #     closed_price,
    #     last_traded_timestamp,
    #     open_interest,
    #     open_interest_change_percentage,
    #     upper_circuit_limit,
    #     lower_circuit_limit,
    #     one_year_week_high_price,
    #     one_year_week_low_price
    #     ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    

    #     value_query = (message["token"], message["sequence_number"],formatted_time, message["last_traded_price"],
    #                 message["last_traded_quantity"], message["average_traded_price"], message["volume_trade_for_the_day"],
    #                 message["total_buy_quantity"], message["total_sell_quantity"], message["open_price_of_the_day"],
    #                 message["high_price_of_the_day"], message["low_price_of_the_day"], message["closed_price"],
    #                 message["last_traded_timestamp"], message["open_interest"], message["open_interest_change_percentage"],
    #                 message["upper_circuit_limit"], message["lower_circuit_limit"], message["52_week_high_price"],
    #                 message["52_week_high_price"])
        
    #     cursor.execute(insert_query, value_query)
    #     conn.commit()
        
    #     best_5_buy_data_insert_query = '''INSERT INTO best_5_buy_data(flag, quantity, price, no_of_orders) VALUES(%s, %s, %s, %s)'''
        # for data in message["best_5_buy_data"]:
        #     flag = data["flag"]
        #     quantity = data["quantity"]
        #     price = data["price"]
        #     no_of_orders = data["no of orders"]

        #     best_5_buy_data_value_query = (flag, quantity, price, no_of_orders)

    #         cursor.execute(best_5_buy_data_insert_query, best_5_buy_data_value_query)
    #         conn.commit()

        
    #     best_5_sell_data_insert_query = '''INSERT INTO best_5_sell_data(flag, quantity, price, no_of_orders) VALUES(%s, %s, %s, %s)'''
    #     for data in message["best_5_sell_data"]:
    #         flag = data["flag"]
    #         quantity = data["quantity"]
    #         price = data["price"]
    #         no_of_orders = data["no of orders"]

    #         best_5_sell_data_value_query = (flag, quantity, price, no_of_orders)

    #         cursor.execute(best_5_sell_data_insert_query, best_5_sell_data_value_query)
    #         conn.commit()

        
    # except psycopg2.Error as e:
    #     conn.rollback()  # Rollback transaction
    #     print(f"Database error occurred: {e}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")

    # last_traded_timestamp = message["exchange_timestamp"] / 1000
    # real_time = datetime.datetime.fromtimestamp(last_traded_timestamp)
    # formatted_time = real_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # # Replace exchange_timestamp with converted timestamp
    # message["exchange_timestamp"] = formatted_time


    # last_traded_timestamp = message["exchange_timestamp"] / 1000
    # real_time = datetime.datetime.fromtimestamp(last_traded_timestamp)
    # formatted_time = real_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # # Replace exchange_timestamp with converted timestamp
    # message["exchange_timestamp"] = formatted_time


    # with open(r"C:\Users\Dell 1\OneDrive\Desktop\angel_api\streaming_data\test_data.csv", 'a', newline='') as csv_file:
    #     writer = csv.DictWriter(csv_file, fieldnames=message.keys())
    #     writer.writeheader()
    #     writer.writerow(message)

        
    # print(message)
    # print("\n")
    try:
        # Convert timestamp
        last_traded_timestamp = message.get("exchange_timestamp", 0) / 1000
        real_time = datetime.datetime.fromtimestamp(last_traded_timestamp)
        formatted_time = real_time.strftime('%Y-%m-%d %H:%M:%S')
        message["exchange_timestamp"] = formatted_time
        
        flat_message = flatten_data(message)

        fieldnames = flat_message.keys()

        # with open(r"C:\Users\Dell 1\OneDrive\Desktop\angel_api\april.csv", "a", newline="") as csv_file:
        #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #     if csv_file.tell() == 0:  # Check if file is empty
        #         writer.writeheader()  # Write header only if the file is empty
        #     writer.writerow(flat_message)
    except Exception as e:
        print(f"An error occurred while writing to the CSV file: {e}")

    print(message)
    print("\n")



def on_open(wsapp):
    print("on open")
    sws.subscribe(correlation_id, mode, token_list)

def on_error(wsapp, error):
    print(error)


def start_websocket():
    print("Market opened. Starting websocket connection")
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.connect()


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(start_websocket)
    # executor.submit(on_data)