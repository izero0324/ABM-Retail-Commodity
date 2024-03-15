from agent_pool.sample_agent import single_random_agent

def agent_choose(agent_name):
    '''
    A gateway to choose from different agents
    '''
    if 'ZIP' in agent_name:
        print("I'm a ZIP agent")
    elif 'ZI' in agent_name:
        print("I'm a ZI agent")
    else:
        print("I'm a Random agent")
        single_random_agent(agent_name)