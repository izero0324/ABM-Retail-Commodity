import random
import numpy as np

from tools.api_interface import post_order
from agent_pool.strategies import Strategies

def single_random_agent(agent_name: str, is_buy: bool):
    side = "B"
    agent_name = agent_name
    agent_q = random.randint(1, 10)
    agent_p = random.randint(80, 120)
    side_rnd = random.randint(0,1)
    if side_rnd == 1:
        side = "S"
    post_order( 1, agent_p, agent_q, agent_name, side) #post_order(1, price, quant,name, Buy/Sell)

def ZI_agent(agent_name, is_buy: bool):
    # Decide if this agent is buyer/seller
    side = 'B' if is_buy else 'S'
    # Initial class `Strategies`
    strat = Strategies()
    strat.init(agent_name, side)
    # Input your strategy here and get return of price and quantity
    side, agent_p, agent_q =  strat.ZI()
    post_order( 1, agent_p, agent_q, agent_name, side) # Post order

def mix_strategy_agent_example(agent_name: str, is_buy: bool):
    # Decide if this agent is buyer/seller
    side = 'B' if is_buy else 'S'
    # Initial class `Strategies`
    strat = Strategies()
    strat.init(agent_name, side)
    # Input your strategy here and get return of price and quantity
    side, agent_p1, agent_q1 =  strat.ZI()
    side, agent_p2, agent_q2 =  strat.ZIP(10)
    # Mix your strategy here
    agent_price = np.mean(agent_p1,agent_p2) 
    agent_quant = np.mean(agent_q1,agent_q2)
    post_order( 1, agent_price, agent_quant, agent_name, side) # Post order





