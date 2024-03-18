import pandas as pd
from tools.sql_connection import DatabaseConnectionManager


def get_price_spread(exp_name):
    with DatabaseConnectionManager() as cursor:
        query = f"SELECT tick, LowestSuccessTradePrice, HighestSuccessTradePrice FROM PriceSpread_{exp_name} ORDER BY tick"
        cursor.execute(query)
        rows = cursor.fetchall()
        
    return pd.DataFrame(rows)


