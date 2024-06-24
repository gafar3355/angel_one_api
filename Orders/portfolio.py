import http.client
import json
from SmartApi import SmartConnect
from pyotp import TOTP


conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")
obj = SmartConnect('4GznkDiG')
data = obj.generateSession('R103352', 7020, TOTP('RV62S7GJBGHGWKRAYSQ6SRTPVM').now())

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


conn.request("GET", "/rest/secure/angelbroking/order/v1/getOrderBook", headers=headers)


res = conn.getresponse()
data = res.read()
# print(data)
# Check if request was successful (HTTP status code 200)
if res.status == 200:
    
    response_data = json.loads(data.decode("utf-8"))
    
    if 'data' in response_data:
        orders = response_data['data']

    for order in orders:
            variety = order.get('variety', '')
            ordertype = order.get('ordertype', '')
            producttype = order.get('producttype', '')
            duration = order.get('duration', '')
            price = order.get('price', '')
            triggerprice = order.get('triggerprice', '')
            quantity = order.get('quantity', '')
            disclosedquantity = order.get('disclosedquantity', '')
            squareoff = order.get('squareoff', '')
            stoploss = order.get('stoploss', '')
            trailingstoploss = order.get('trailingstoploss', '')
            tradingsymbol = order.get('tradingsymbol', '')
            transactiontype = order.get('transactiontype', '')
            exchange = order.get('exchange', '')
            symboltoken = order.get('symboltoken', '')
            instrumenttype = order.get('instrumenttype', '')
            strikeprice = order.get('strikeprice', '')
            optiontype = order.get('optiontype', '')
            expirydate = order.get('expirydate', '')
            lotsize = order.get('lotsize', '')
            cancelsize = order.get('cancelsize', '')
            averageprice = order.get('averageprice', '')
            filledshares = order.get('filledshares', '')
            unfilledshares = order.get('unfilledshares', '')
            orderid = order.get('orderid', '')
            text = order.get('text', '')
            status = order.get('status', '')
            orderstatus = order.get('orderstatus', '')
            updatetime = order.get('updatetime', '')
            exchtime = order.get('exchtime', '')
            exchorderupdatetime = order.get('exchorderupdatetime', '')
            fillid = order.get('fillid', '')
            filltime = order.get('filltime', '')
            parentorderid = order.get('parentorderid', '')
            uniqueorderid = order.get('uniqueorderid', '')

            
            print(f"Order ID: {orderid}")
            # print(f"Variety: {variety}")
            print(f"Order Type: {ordertype}")
            print(f"Product Type: {producttype}")
            # print(f"Duration: {duration}")
            print(f"Price: {price}")
            # print(f"Trigger Price: {triggerprice}")
            print(f"Quantity: {quantity}")
            # print(f"Disclosed Quantity: {disclosedquantity}")
            # print(f"Square Off: {squareoff}")
            # print(f"Stop Loss: {stoploss}")
            # print(f"Trailing Stop Loss: {trailingstoploss}")
            print(f"Trading Symbol: {tradingsymbol}")
            print(f"Transaction Type: {transactiontype}")
            # print(f"Exchange: {exchange}")
            # print(f"Symbol Token: {symboltoken}")
            # print(f"Instrument Type: {instrumenttype}")
            # print(f"Strike Price: {strikeprice}")
            # print(f"Option Type: {optiontype}")
            # print(f"Expiry Date: {expirydate}")
            # print(f"Lot Size: {lotsize}")
            # print(f"Cancel Size: {cancelsize}")
            print(f"Average Price: {averageprice}")
            # print(f"Filled Shares: {filledshares}")
            # print(f"Unfilled Shares: {unfilledshares}")
            # print(f"Text: {text}")
            # print(f"Status: {status}")
            print(f"Order Status: {orderstatus}")
            print(f"Update Time: {updatetime}")
            # print(f"Exchange Time: {exchtime}")
            # print(f"Exchange Order Update Time: {exchorderupdatetime}")
            # print(f"Fill ID: {fillid}")
            # print(f"Fill Time: {filltime}")
            # print(f"Parent Order ID: {parentorderid}")
            # print(f"Unique Order ID: {uniqueorderid}")
            print("------------------------------")

else:
    print(f"Error fetching data. Status code: {res.status}")

conn.close()
