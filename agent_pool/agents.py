from tools.api_interface import post_order
from agent_pool.strategies import Strategies
import random
import numpy as np

def ZI_agent(agent_name, is_buy: bool):
    side = 'B' if is_buy else 'S'
    strat = Strategies()
    strat.init(agent_name, side)
    side, agent_p, agent_q =  strat.ZI()
    post_order( 1, agent_p, agent_q, agent_name, side) 

def ZIP_agent(agent_name, GreedyLevel, is_buy:bool ):
    side = 'B' if is_buy else 'S'
    strat = Strategies()
    strat.init(agent_name, side)
    side, agent_p, agent_q =  strat.ZIP(GreedyLevel)
    post_order( 1, agent_p, agent_q, agent_name, side) #post_order(1, price, quant,name, Buy/Sell)

def market_demand_agent(agent_name, is_buy:bool ):
    side = 'B' if is_buy else 'S'
    strat = Strategies()
    strat.init(agent_name, side)
    side, agent_p, agent_q  = strat.dynamic_pricing_strategy()
    post_order( 1, agent_p, agent_q, agent_name, side) 

def penetration_agent(agent_name,is_buy:bool ):
    side = 'B' if is_buy else 'S'
    strat = Strategies()
    strat.init(agent_name,side)
    side, agent_p, agent_q  = strat.penetration()
    post_order( 1, agent_p, agent_q, agent_name, side) 

def dynamic_sell_agent(agent_name, is_buy: bool ):
    if not is_buy: side='S'
    strat = Strategies()
    strat.init(agent_name,side)
    side, agent_p, agent_q  = strat.dynamic()
    post_order( 1, agent_p, agent_q, agent_name, side) 

def decide_trend_agent(agent_name,is_buy:bool ):
    side = 'B' if is_buy else 'S'
    strat = Strategies()
    strat.init(agent_name,side)
    side, agent_p, agent_q  = strat.decide_order_trend_strategy()
    post_order( 1, agent_p, agent_q, agent_name, side) 