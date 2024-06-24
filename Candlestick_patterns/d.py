import pandas as pd
import time
from datetime import datetime

def analyze_candlestick_data(file_path):
    df = pd.read_csv(file_path)

    def check_marubozu(row):
        if row['high'] == row['close'] or row['open'] < row['close']:
            return 1   # Bullish
        elif row['low'] == row['close'] or row['open'] > row['close']:
            return 0   # Bearish
        else:
            return None  # Not a marubozu
        
    df['marubozu'] = df.apply(check_marubozu, axis=1)

    def is_spinning_top(row):
        body_length = abs(row['close'] - row['open'])
        total_range = row['high'] - row['low']
        return body_length / total_range < 0.3
        # if total_range != 0:  # Add this check
        #     return body_length / total_range < 0.3
        # else:
        #     return False

    df['spinning_top'] = df.apply(is_spinning_top, axis=1)

    def is_hammer(row):
        body_length = abs(row['close'] - row['open'])
        upper_shadow = row['high'] - max(row['open'], row['close'])
        lower_shadow = min(row['open'], row['close']) - row['low']
        return lower_shadow >= 2 * body_length and upper_shadow <= 0.1 * body_length

    df['hammer'] = df.apply(is_hammer, axis=1)

    def is_doji(row):                                               
        body_length = abs(row['close'] - row['open'])
        total_range = row['high'] - row['low']
        return body_length / total_range < 0.1 and row['close'] == row['open']
        # if total_range != 0:  # Add this check
        #     return body_length / total_range < 0.1 and row['close'] == row['open']
        # else:
        #     return False

    df['doji'] = df.apply(is_doji, axis=1)

    def is_shooting_star(row):
        body_length = abs(row['close'] - row['open'])
        upper_shadow = row['high'] - max(row['open'], row['close'])    # upper shadow is greater than or equal to twice the length of the body 
        lower_shadow = min(row['open'], row['close']) - row['low']     #The lower shadow is less than or equal to 10% of the length of the body
        return upper_shadow >= 2 * body_length and lower_shadow <= 0.1 * body_length
    
    df['shooting_star']=df.apply(is_shooting_star,axis=1)

    new_df = df[(df[['doji', 'hammer', 'spinning_top','shooting_star']] == True).any(axis=1)]

    # return new_df.to_string(index=False)
    return new_df.to_csv(r'C:\Users\Dell 1\OneDrive\Desktop\angel_api\Hammer_Patterns\Anaylsis\icici_data.csv',index=False)


file_paths = {
    'Axis BNK': r"C:\Users\Dell 1\OneDrive\Desktop\Jump Analysis\Analysis_Data\axis.csv",
    'Federal BNK': r"C:\Users\Dell 1\OneDrive\Desktop\Jump Analysis\Analysis_Data\federal.csv",
    'HDFC BNK': r"C:\Users\Dell 1\OneDrive\Desktop\Jump Analysis\Analysis_Data\hdfc.csv",
    'SBIN BNK': r"C:\Users\Dell 1\OneDrive\Desktop\Jump Analysis\ok_data2.csv",
    'ICICI BNK': r"C:\Users\Dell 1\OneDrive\Desktop\Jump Analysis\Analysis_Data\icici.csv"
}

# Analyze each file and print the result
while True:
    print("Time :", datetime.now().strftime("%Y-%m-%d %H:%M"))
    for bank,file_path in file_paths.items():
        print("///////////////////////////////////////////////////////////////")
        print("Analyzing:", bank)
        result_df = analyze_candlestick_data(file_path)
        print(result_df)
        print("\n")
    time.sleep(30)

