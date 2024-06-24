import http.client
import json
from SmartApi import SmartConnect
from pyotp import TOTP

conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
obj = SmartConnect('4GznkDiG')
data = obj.generateSession('R103352', 7020, TOTP('RV62S7GJBGHGWKRAYSQ6SRTPVM').now())

payload = {
    "variety": "NORMAL",
    "tradingsymbol": "SBIN-EQ",
    "symboltoken": "3045",
    "transactiontype": "BUY",
    "exchange": "NSE",
    "ordertype": "MARKET",
    "producttype": "INTRADAY",
    "duration": "DAY",
    "price": "194.50",
    "squareoff": "0",
    "stoploss": "0",
    "quantity": "1"
}

payload_json = json.dumps(payload)

headers = {
    'Authorization': data["data"]["jwtToken"],
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
    'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
    'X-MACAddress': 'MAC_ADDRESS',
    'X-PrivateKey': '4GznkDiG'
}

url = "/rest/secure/angelbroking/order/v1/placeOrder"

conn.request("POST", url, payload_json, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
