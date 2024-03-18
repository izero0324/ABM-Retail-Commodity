import pandas as pd
from tools.sql_connection import DatabaseConnectionManager


def get_price_spread(exp_name):
    with DatabaseConnectionManager() as cursor:
        query = f"SELECT tick, LowestSuccessTradePrice, HighestSuccessTradePrice \
            FROM PriceSpread_{exp_name} ORDER BY tick"
        cursor.execute(query)
        rows = cursor.fetchall()
        
    return pd.DataFrame(rows)

def get_total_ticks(exp_name):
    with DatabaseConnectionManager() as cursor:
        query = f"SELECT MAX(tick) FROM OrderBook_{exp_name}"
        cursor.execute(query)
        tick_num = cursor.fetchall()
    return tick_num[0][0]

def get_all_traded_pxq_at_tick(exp_name, tick):
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
    ticks = get_total_ticks(exp_name)
    traded = 0
    ordered = 0
    for tick in range(ticks+1):
        traded += get_all_traded_pxq_at_tick(exp_name, tick)
        ordered += get_all_ordered_pxq_at_tick(exp_name, side, tick)
    return traded/ordered

def AgentLossRatio(exp_name, agent_name):
    ticks = get_total_ticks(exp_name)
    traded = 0
    ordered = 0
    for tick in range(ticks+1):
        traded += get_agent_traded_pxq_at_tick(exp_name,agent_name, tick)
        ordered += get_agent_ordered_pxq_at_tick(exp_name, agent_name, tick)
    return traded/ordered
    