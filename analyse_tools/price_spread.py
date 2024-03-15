import pandas as pd
import matplotlib.pyplot as plt
from tools.sql_connection import DatabaseConnectionManager



def get_price_spread(exp_name):
    with DatabaseConnectionManager() as cursor:
        query = f"SELECT tick, LowestSuccessTradePrice, HighestSuccessTradePrice FROM PriceSpread_{exp_name} ORDER BY tick"
        cursor.execute(query)
        rows = cursor.fetchall()
        
    return pd.DataFrame(rows)


def plot_price_spread(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df[0], df[1], label='LowestSuccessTradePrice', linestyle='-')
    plt.plot(df[0], df[2], label='HighestSuccessTradePrice', linestyle='-')
    
    plt.title('Price Spread Over Ticks')
    plt.xlabel('Tick')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

