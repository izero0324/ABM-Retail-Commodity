import pandas as pd
from tools.sql_connection import DatabaseConnectionManager

def fetch_df_by_sql(SQL_string):
    with DatabaseConnectionManager() as cursor:
        cursor.execute(SQL_string)
        rows = cursor.fetchall()
    return rows


def hist_n_order_by_agent(exp_name, agent_name, n):
    '''
    Input:
    exp_name: str #the experiment name
    agent_name : str #the agent who's checking 
    n: int #the last n day to get
    Output:
    The last n order that agent made
    '''
    query = f"SELECT * FROM OrderBook_{exp_name} WHERE agent_name='{agent_name}' Order by tick DESC limit {n}"
    return fetch_df_by_sql(query)


def hist_n_price(exp_name, n):
    '''
    Input: 
    exp_name: str #the experiment name
    n: int #the last n day to get
    Output:
    n day of price spread, by the order of reversed time (The first one will be today)
    '''
    query = f"SELECT LowestSuccessTradePrice, HighestSuccessTradePrice FROM PriceSpread_{exp_name} ORDER BY tick DESC limit {n}"
    return fetch_df_by_sql(query)

def hist_n_trade_by_agent(exp_name, agent_name, n):
    '''
    Input:
    exp_name: str #the experiment name
    agent_name : str #the agent who's checking 
    n: int #the last n day to get
    Output:
    Success trades in the last n tick order that agent made
    '''
    query = f"SELECT * FROM SuccessTrade_{exp_name} Where (buy_agent='{agent_name}' or sell_agent='{agent_name}') \
        and tick > (SELECT tick from OrderBook_{exp_name} Order by tick Desc limit 1)-{n} \
        Order by tick DESC;"
    return fetch_df_by_sql(query)