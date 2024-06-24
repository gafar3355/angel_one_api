import http.client
from SmartApi import SmartConnect
from pyotp import TOTP
import json
import csv
import time

conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
# symbol_tokens = [
#     13786, 1964, 11403, 9552, 3150, 4684, 1901, 17963, 13, 3103, 3518, 7929,
#     11195, 2303, 1406, 6545, 24184, 13611, 10099, 15380, 19913, 4745, 8479,
#     1232, 10440, 526, 694, 22377, 15083, 25780, 14309, 1270, 16675, 15141,
#     4244, 10604, 3351, 3220, 1624, 17400, 2142, 10666, 312, 547, 9819, 21770,
#     4306, 685, 10447, 2277, 21808, 10940, 2181, 11703, 2664, 25, 22, 20374,
#     13285, 11373, 20242, 14592, 1633, 11532, 23650, 15355, 3563, 11184, 275,
#     10753, 2535, 14418, 760, 881, 438, 17094, 9590, 10217, 7229, 14732, 1023,
#     4668, 21238, 11536, 1660, 9599, 212, 14413, 3411, 2029, 10243, 13751,
#     5900, 2885, 1997, 9480, 910, 772, 317, 2144, 404, 157, 467, 17029,
#     14299, 3506, 236, 8075, 21690, 1363, 18652, 2043, 3812, 958, 3045, 11723,
#     4963, 3787, 18564, 11630, 422, 4749, 20302, 3721, 13538, 739, 1394, 17875,
#     11915, 2475, 6066, 305, 17818, 10794, 18921, 21614, 30108, 17971, 2031,
#     1186, 1922, 1348, 383, 4067, 14672, 17438, 3273, 371, 11483, 1333, 13750,
#     13404, 19943, 10999, 11543, 11262, 16965, 509, 3456, 5373, 6733, 11654,
#     16713, 11287, 11351, 17869, 18365, 5258, 2963, 8110, 3063, 18096, 3718,
#     14977, 19234, 1594, 1512, 14366, 335, 4503, 6656, 16669, 6705, 2263, 2412,
#     3426, 9683, 3499, 10599, 4717, 1008, 15332, 8596, 163, 24948, 4204, 29135,
#     5097, 3432, 3405
# ]
symbol_tokens=[2181,10794,3518,9819,157,1270,3351,16669,383,1624,13538,10666,4717,526,18143]
obj = SmartConnect('4GznkDiG')
data = obj.generateSession('R103352', 7020, TOTP('RV62S7GJBGHGWKRAYSQ6SRTPVM').now())

headers = {
    'X-PrivateKey': '4GznkDiG',
    'Accept': 'application/json',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
    'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
    'X-MACAddress': 'MAC_ADDRESS',
    'X-UserType': 'USER',
    'Authorization': data["data"]["jwtToken"],
    'Content-Type': 'application/json'
}
from_date = "2019-01-01 09:15"
to_date = "2023-12-30 15:30"


with open(r'C:\Users\Dell 1\OneDrive\Desktop\angel_api\company data\historical\stocks_15.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    
    writer.writerow(['Token', 'Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

    for symbol_token in symbol_tokens:
        payload = {
            "exchange": "NSE",
            "symboltoken": symbol_token,
            "interval": "ONE_DAY",
            "fromdate": from_date,
            "todate": to_date
        }

        while True:
            try:
                conn.request("POST", "/rest/secure/angelbroking/historical/v1/getCandleData", json.dumps(payload), headers)
                res = conn.getresponse()
                response_data = res.read().decode("utf-8")
                json_data = json.loads(response_data)

                
                for record in json_data['data']:
                    writer.writerow([symbol_token] + record)

                print(f"Token: {symbol_token} - Data written to CSV")
                print("------------------------------------------")
                break
            except Exception as e:
                print(f"Exception: {e}")
                print("Retrying after 3 seconds...")  #delay to 3 seconds
                time.sleep(3)  


conn.close()



