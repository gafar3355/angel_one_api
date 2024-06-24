import pandas as pd

# Pivot points from 29/05/2024
pivot_levels = {
    "PP": 5909.78,
    "R_1": 5938.66,
    "S_1": 5874.56,
    "R_2": 5973.88,
    "S_2": 5845.68,
    "R_3": 6002.76,
    "S_3": 5810.46,
}


data = pd.read_csv(r'C:\Users\Dell 1\OneDrive\Desktop\angel_api\company data\historical\apollo_30.csv')

# Checking  each data point crosses any pivot point/support/resistance
crossed_levels = []

for index, row in data.iterrows():
    high = row['high']
    low = row['low']
    crosses = []
    
    for level_name, level_value in pivot_levels.items():
        if low <= level_value <= high:
            crosses.append(level_name)
    
    crossed_levels.append(crosses)


data['crossed_levels'] = crossed_levels
data.to_csv(r"C:\Users\Dell 1\OneDrive\Desktop\angel_api\Indicators\appl.csv",index=False)

# print(data[['Timestamp', 'high', 'low', 'crossed_levels']])

