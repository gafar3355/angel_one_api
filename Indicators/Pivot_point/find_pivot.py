
def calculate_pivot_point(high, low, close):
    
    # high : High price of the previous trading day.
    # low : Low price of the previous trading day.
    # close : Closing price of the previous trading day.

    pivot_point = (high + low + close) / 3
    
    resistance_1 = (2 * pivot_point) - low
    support_1 = (2 * pivot_point) - high
    
    resistance_2 = pivot_point + (high - low)
    support_2 = pivot_point - (high - low)
    
    resistance_3 = high + 2 * (pivot_point - low)
    support_3 = low - 2 * (high - pivot_point)
    
    return {
        "PP": pivot_point,
        "R_1": resistance_1,
        "S_1": support_1,
        "R_2": resistance_2,
        "S_2": support_2,
        "R_3": resistance_3,
        "S_3": support_3,
    }

# APOLLOHOS 29/05/2024                                             
high = 5945
low = 5880.90
close = 5903.45

pivot_levels = calculate_pivot_point(high, low, close)
print(pivot_levels)



# OUTPUT APOLLOHOS 30/05/2024 

# {'pivot_point': 5909.783333333333, 
#  'resistance_1': 5938.666666666666, 
#  'support_1': 5874.566666666666, 
#  'resistance_2': 5973.883333333333,
#  'support_2': 5845.6833333333325, 
#  'resistance_3': 6002.766666666666, 
#  'support_3': 5810.466666666665}