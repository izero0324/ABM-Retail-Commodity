from agent_pool.sample_agent import single_random_agent
from agent_pool.agents import *

def agent_choose(agent_name):
    '''
    A gateway to choose from different agents
    '''
    is_buy = 'B' in agent_name

    if 'ZIP' in agent_name:
        ZIP_agent(agent_name, 10, is_buy=is_buy)

    elif 'ZI' in agent_name:
        ZI_agent(agent_name, is_buy=is_buy)

    elif 'MD' in agent_name:
        market_demand_agent(agent_name,is_buy=is_buy)

    elif 'PN' in agent_name:
        penetration_agent(agent_name,is_buy=is_buy)
    
    elif 'DYN' in agent_name:
        print("[Agent] I'm a DYN sell agent")
        dynamic_sell_agent(agent_name,is_buy=False)
    
    elif 'DT' in agent_name:
        decide_trend_agent(agent_name,is_buy=is_buy)

    else:
        print("[Agent] I'm a Random agent")
        single_random_agent(agent_name)