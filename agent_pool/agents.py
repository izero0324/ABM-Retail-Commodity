from tools.api_interface import post_order
from agent_pool.strategies import Strategies
import random
import numpy as np

def ZI_buy_agent(agent_name):
    strat = Strategies()
    strat.init(agent_name, 'B')
    side, agent_p, agent_q =  strat.ZI()
    post_order( 1, agent_p, agent_q, agent_name, side) #post_order(1, price, quant,name, Buy/Sell)

def ZI_sell_agent(agent_name):
    strat = Strategies()
    strat.init(agent_name, 'S')
    side, agent_p, agent_q =  strat.ZI()
    post_order( 1, agent_p, agent_q, agent_name, side) #post_order(1, price, quant,name, Buy/Sell)

def ZIP_buy_agent(agent_name):
    strat = Strategies()
    strat.init(agent_name, 'B')
    side, agent_p, agent_q =  strat.ZIP(10)
    post_order( 1, agent_p, agent_q, agent_name, side) #post_order(1, price, quant,name, Buy/Sell)

def ZIP_sell_agent(agent_name):
    strat = Strategies()
    strat.init(agent_name, 'S')
    side, agent_p, agent_q =  strat.ZIP(10)
    post_order( 1, agent_p, agent_q, agent_name, side) #post_order(1, price, quant,name, Buy/Sell)

def market_demand_buy_agent(agent_name):
    strat = Strategies()
    strat.init(agent_name,'B')
    side, agent_p, agent_q  = strat.dynamic_pricing_strategy()
    post_order( 1, agent_p, agent_q, agent_name, side) 

def market_demand_sell_agent(agent_name):
    B1 = Strategies()
    B1.init(agent_name,'S')
    side, agent_p, agent_q  = B1.dynamic_pricing_strategy()
    post_order( 1, agent_p, agent_q, agent_name, side) 

def penetration_buy_agent(agent_name):
    strat = Strategies()
    strat.init(agent_name,'B')
    side, agent_p, agent_q  = strat.penetration()
    post_order( 1, agent_p, agent_q, agent_name, side) 

def penetration_sell_agent(agent_name):
    strat = Strategies()
    strat.init(agent_name,'S')
    side, agent_p, agent_q  = strat.penetration()
    post_order( 1, agent_p, agent_q, agent_name, side) 

def dynamic_sell_agent(agent_name):
    strat = Strategies()
    strat.init(agent_name,'S')
    side, agent_p, agent_q  = strat.dynamic()
    post_order( 1, agent_p, agent_q, agent_name, side) 

def decide_trend_buy_agent(agent_name):
    strat = Strategies()
    strat.init(agent_name,'B')
    side, agent_p, agent_q  = strat.decide_order_trend_strategy()
    post_order( 1, agent_p, agent_q, agent_name, side) 

def decide_trend_sell_agent(agent_name):
    strat = Strategies()
    strat.init(agent_name,'S')
    side, agent_p, agent_q  = strat.decide_order_trend_strategy()
    post_order( 1, agent_p, agent_q, agent_name, side) 