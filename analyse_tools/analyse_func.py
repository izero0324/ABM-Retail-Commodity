import pandas as pd
from tools.sql_connection import DatabaseConnectionManager


def get_price_spread(exp_name):
    '''
    return the price spread dataframe by exp_name
    Input:
    exp_name(str) : selected exp name
    Return:
    PriceSpread(df) : dataframe of price spread by tick
    '''
    with DatabaseConnectionManager() as cursor:
        query = f"SELECT tick, LowestSuccessTradePrice, HighestSuccessTradePrice \
            FROM PriceSpread_{exp_name} ORDER BY tick"
        cursor.execute(query)
        rows = cursor.fetchall()
        
    return pd.DataFrame(rows)

def get_total_ticks(exp_name):
    '''
    Count total ticks from exp_name
    Input:
    exp_name(str) : selected exp name
    Return:
    tick_num(int)
    '''
    with DatabaseConnectionManager() as cursor:
        query = f"SELECT MAX(tick) FROM OrderBook_{exp_name}"
        cursor.execute(query)
        tick_num = cursor.fetchall()
    return tick_num[0][0]

def get_all_traded_pxq_at_tick(exp_name, tick):
    '''
    Calculate Sussfully traded price x quantity in a tick by exp_name
    Input:
    exp_name(str) : selected exp name
    tick(int) 
    Return:
    cum_prod(float)
    '''
    cum_prod = 0
    with DatabaseConnectionManager() as cursor:
        query = f"SELECT trade_price, quantity FROM SuccessTrade_{exp_name} WHERE tick={tick};"
        cursor.execute(query)
        rows = cursor.fetchall()
    for row in rows:
        #print(row)
        cum_prod += (row[0] * row[1])
    return cum_prod

def get_all_ordered_pxq_at_tick(exp_name, side, tick):
    '''
    Calculate Ordered price x quantity in a tick by exp_name
    Input:
    exp_name(str) : selected exp name
    side(str) : 'Buy' or 'Sell'
    tick(int) 
    Return:
    cum_prod(float)
    '''
    cum_prod = 0
    with DatabaseConnectionManager() as cursor:
        query = f" SELECT trade_price, quantity FROM OrderBook_{exp_name} \
            WHERE (agent_name LIKE '%{side}%') AND tick={tick};"
        cursor.execute(query)
        rows = cursor.fetchall()
    for row in rows:
        #print(row)
        cum_prod += (row[0] * row[1])
    return cum_prod

def get_agent_traded_pxq_at_tick(exp_name, agent_name, tick):
    '''
    Calculate single agent success traded price x quantity in a tick by exp_name
    Input:
    exp_name(str) : selected exp name
    agent_name(str)
    tick(int) 
    Return:
    cum_prod(float)
    '''
    cum_prod = 0
    with DatabaseConnectionManager() as cursor:
        query = f"SELECT trade_price, quantity FROM SuccessTrade_{exp_name} \
            WHERE tick={tick} AND (buy_agent='{agent_name}' OR sell_agent='{agent_name}');"
        #print(query)
        cursor.execute(query)
        rows = cursor.fetchall()
    for row in rows:
        #print(row)
        cum_prod += (row[0] * row[1])
    return cum_prod

def get_agent_ordered_pxq_at_tick(exp_name, agent_name, tick):
    '''
    Calculate single agent ordered price x quantity in a tick by exp_name
    Input:
    exp_name(str) : selected exp name
    agent_name(str)
    tick(int) 
    Return:
    cum_prod(float)
    '''
    cum_prod = 0
    with DatabaseConnectionManager() as cursor:
        query = f" SELECT trade_price, quantity FROM OrderBook_{exp_name} \
            WHERE (agent_name='{agent_name}' AND tick={tick});"
        cursor.execute(query)
        rows = cursor.fetchall()
    for row in rows:
        #print(row)
        cum_prod += (row[0] * row[1])
    return cum_prod

def AllLossRatio(exp_name, side='Buy'):
    '''
    SUM(All tick Traded Quantity * Price) / SUM(All tick Buyer's(or Seller) Order Quantity * Price)
    Input:
    exp_name(str)
    side(str) : 'Buy' or 'Sell'
    Return:
    ratio(float)
    '''
    ticks = get_total_ticks(exp_name)
    traded = 0
    ordered = 0
    for tick in range(ticks+1):
        traded += get_all_traded_pxq_at_tick(exp_name, tick)
        ordered += get_all_ordered_pxq_at_tick(exp_name, side, tick)
    return traded/ordered

def AgentLossRatio(exp_name, agent_name):
    '''
    SUM(An Agent all tick Traded Quantity * Price) / SUM(An Agetn all tick Buyer's(or Seller) Order Quantity * Price)
    Input:
    exp_name(str)
    agent_name(str)
    Return:
    ratio(float)
    '''
    ticks = get_total_ticks(exp_name)
    traded = 0
    ordered = 0
    for tick in range(ticks+1):
        traded += get_agent_traded_pxq_at_tick(exp_name,agent_name, tick)
        ordered += get_agent_ordered_pxq_at_tick(exp_name, agent_name, tick)
    return traded/ordered
    