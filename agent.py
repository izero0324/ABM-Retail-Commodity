from market_env.api_interface import post_order
import random
import numpy as np


def random_agent(agent_id):
    #historical_price(days, agent_id)
    agent_num = 10
    agent_pool = np.arange(0, agent_num, 1).tolist()
    side = "B"
    for agent in agent_pool:
        agent_name = 'B000'+str(agent)
        agent_q = random.randint(1, 10)
        agent_p = random.randint(97, 103)
        side_rnd = random.randint(0,1)
        if side_rnd == 1:
            side = "S"
        post_order( 1, agent_p, agent_q, agent_name, side)
