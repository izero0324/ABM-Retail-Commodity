from agent_pool.sample_agent import single_random_agent
from agent_pool.agents import *

def agent_choose(agent_name):
    '''
    A gateway to choose from different agents
    '''
    if 'ZIP' in agent_name:
        if 'B' in agent_name:
            print("[Agent] I'm a ZIP buy agent")
            ZIP_buy_agent(agent_name)
        else:
            print("[Agent] I'm a ZIP sell agent")
            ZIP_sell_agent(agent_name)

    elif 'ZI' in agent_name:
        if 'B' in agent_name:
            print("[Agent] I'm a ZI buy agent")
            ZI_buy_agent(agent_name)
        else:
            print("[Agent] I'm a ZI sell agent")
            ZI_sell_agent(agent_name)

    elif 'MD' in agent_name:
        if 'B' in agent_name:
            print("[Agent] I'm a MD buy agent")
            market_demand_buy_agent(agent_name)
        else:
            print("[Agent] I'm a MD sell agent")
            market_demand_sell_agent(agent_name)

    elif 'PN' in agent_name:
        if 'B' in agent_name:
            print("[Agent] I'm a PN buy agent")
            penetration_buy_agent(agent_name)
        else:
            print("[Agent] I'm a PN sell agent")
            penetration_sell_agent(agent_name)
    
    elif 'DYN' in agent_name:
        print("[Agent] I'm a DYN sell agent")
        dynamic_sell_agent(agent_name)
    
    elif 'DT' in agent_name:
        if 'B' in agent_name:
            print("[Agent] I'm a DT buy agent")
            decide_trend_buy_agent(agent_name)
        else:
            print("[Agent] I'm a DT sell agent")
            decide_trend_sell_agent(agent_name)

    else:
        print("[Agent] I'm a Random agent")
        single_random_agent(agent_name)