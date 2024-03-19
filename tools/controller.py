from agent_pool.agent_controller import agent_choose
from tools.p_mech import pairing
from tools.api_interface import post_clear_order, get_temp_order_book
import sys
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



def state_now():
    for key, value in state_machine.items():
        try:
            if value == True:
                return key
        except:
            raise ValueError("[Controller] State machine Error")

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
        raise IndexError("[Controller] State Machine Next State failed")


def get_orders(agent_list):
    for agent in agent_list:
        print("[Controller] call ", agent, "to start posting order!")
        try:
            agent_choose(agent)
            print("[Controller] Get return from agent ", agent,", next agent ready...")
        except:
            print("[Controller] Agent ", agent, " failed to retrun order")

def check_orders(agent_list):
    print("[Controller] Checking Orders...")
    order_book = get_temp_order_book()
    done_agents = [order['agent_name'] for order in order_book]
    for agent in agent_list:
        if not agent in done_agents:
            print("[Controller] Retry call agent:", agent)
            agent_choose(agent)
    print("[Controller] All agents posted!(Or Retried)")

def controller(agent_list, tick_num, api_connection, exp_name, main_log):
    post_clear_order()
    
    for tick in range(tick_num):
        print(f"================ tick {tick} ===========================")
        assert state_now() == "Get_order" 
        get_orders(agent_list)
        next_state()
        assert state_now() == "Check_order"
        check_orders(agent_list)
        next_state()
        assert state_now() == "Pairing"
        pairing(api_connection, tick, exp_name)
        next_state()
        assert state_now() == "Check_pair"
        next_state()
        post_clear_order()
        sys.stdout = sys.__stdout__
        print(f"{tick}/{tick_num} DONE")
        sys.stdout = main_log
        

        

    
