from tools.api_interface import post_order
import random
import numpy as np

def single_random_agent(agent_name):
    side = "B"
    agent_name = agent_name
    agent_q = random.randint(1, 10)
    agent_p = random.randint(80, 120)
    side_rnd = random.randint(0,1)
    if side_rnd == 1:
        side = "S"
    post_order( 1, agent_p, agent_q, agent_name, side) #post_order(1, price, quant,name, Buy/Sell)