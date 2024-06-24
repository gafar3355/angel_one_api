import pandas as pd

df = pd.read_csv(r"c:\Users\Dell 1\Downloads\april_22.csv")
df['exchange_timestamp'] = pd.to_datetime(df['exchange_timestamp'])

start_time = pd.Timestamp(df['exchange_timestamp'].dt.date.min()) + pd.Timedelta(hours=9, minutes=15)
end_time = pd.Timestamp(df['exchange_timestamp'].dt.date.min()) + pd.Timedelta(hours=15, minutes=30)  

interval_index = pd.date_range(start=start_time, end=end_time, freq='1min')

aggregated_data = []

for token in df['token'].unique():
    token_df = df[df['token'] == token]
    
    for start_interval, end_interval in zip(interval_index[:-1], interval_index[1:]):
        filtered_df = token_df[(token_df['exchange_timestamp'] >= start_interval) & (token_df['exchange_timestamp'] < end_interval)]
        # print(f"For token {token}, interval {start_interval} - {end_interval}, number of rows: {len(filtered_df)}")
        
        if not filtered_df.empty:
            first_open_price_of_the_minute = filtered_df['last_traded_price'].iloc[0]
            last_closed_price_of_the_minute = filtered_df['last_traded_price'].iloc[-1]
            highest_last_traded_price = filtered_df['last_traded_price'].max()
            lowest_last_traded_price = filtered_df['last_traded_price'].min()
            # total_volume = filtered_df['volume_trade_for_the_day'].iloc[-1] - filtered_df['volume_trade_for_the_day'].iloc[0]
            # starting_vol=filtered_df['volume_trade_for_the_day'].iloc[0]
            # ending_vol=filtered_df['volume_trade_for_the_day'].iloc[-1]
        
            aggregated_data.append({'Token': token, 'Start': start_interval,
                                    # 'End': end_interval,
                                    'open': first_open_price_of_the_minute,
                                    'close': last_closed_price_of_the_minute,
                                    'high': highest_last_traded_price,
                                    'low': lowest_last_traded_price
                                    # 'Total_Volume': total_volume,
                                    # 'End_vol': ending_vol,
                                    # 'Start_vol': starting_vol
                                    })

aggregated_df = pd.DataFrame(aggregated_data)

# print(aggregated_df)
aggregated_df.to_csv(r'C:\Users\Dell 1\OneDrive\Desktop\angel_api\candle_data\april_22_candle.csv',index=False)
