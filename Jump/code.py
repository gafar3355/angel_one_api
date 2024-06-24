import pandas as pd

df=pd.read_csv(r'C:\Users\Dell 1\OneDrive\Desktop\Jump Analysis\dataset\may_03.csv',index_col=False)

k=df[['exchange_timestamp','token','last_traded_price','best_5_buy_data','best_5_sell_data']]

def extract_prices(data_string):
    return [entry['price'] for entry in eval(data_string)]


k['buy_prices'] = k['best_5_buy_data'].apply(extract_prices)
k['sell_prices'] = k['best_5_sell_data'].apply(extract_prices)


def calculate_price_diff(prices):
    price_diff = []
    for i in range(len(prices) - 1):
        diff = prices[i] - prices[i + 1]
        if diff > 5 or diff < -5:           #Threshold = >5  and  < -5
            price_diff.append(diff)
    return price_diff

    

k['buy_price_diff'] = k['buy_prices'].apply(calculate_price_diff)
k['sell_price_diff'] = k['sell_prices'].apply(calculate_price_diff)


# print(k[['buy_prices', 'buy_price_diff', 'sell_prices', 'sell_price_diff']])

k.to_csv(r'C:\Users\Dell 1\OneDrive\Desktop\angel_api\Jump\may3_jump.csv',index=False)



