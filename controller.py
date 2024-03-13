from agent import random_agent
'''
A finite state machine controlling the flow of simulation
1. Call agents to post orders
2. Check if all post are done
3. Call Limit order book to pair
4. Check if the pairing is done
'''
state_machine = {
    "Get_order" : True,
    "Check_order" : False,
    "Pairing": False,
    "Check_pair": False
}

def init():
    agent_list = ('agent1', 'agent2')
    tick_num = 2
    api_connection = 'http://0.0.0.0:8000/'
    return agent_list, tick_num, api_connection

def state_now():
    for key, value in state_machine.items():
        try:
            if value == True:
                return key
        except:
            raise ValueError("State machine Error")

def next_state():
    try:
        keyList=list(state_machine.keys())
        state = state_now()
        index = keyList.index(state)
        try:
            next_index = keyList[index+1]
        except:
            next_index = keyList[0]
        state_machine[state] = False
        state_machine[next_index] = True
        return 0
    except:
        raise IndexError("State Machine Next State failed")


def get_orders(agent_list):
    for agent in agent_list:
        print("call ", agent, "to start posting order!")
        try:
            random_agent()
            print("Get return from agent ", agent,", next agent ready...")
        except:
            print("Agent ", agent, " failed to retrun order")


if __name__ == '__main__':
    agent_list, tick_num, api_connection = init()
    for tick in range(tick_num):
        assert state_now() == "Get_order" 
        get_orders(agent_list)
        next_state()
        assert state_now() == "Check_order"
        next_state()
        assert state_now() == "Pairing"
        next_state()
        assert state_now() == "Check_pair"
        next_state()
    
