from tools.controller import controller
from tools.sql_connection import DatabaseConnectionManager, create_or_truncate_tables
import json

def add_agents(n, agent_list):
    with open('agent_setup.json', 'r') as file:
        agents = json.load(file)

    for agent, value in agents.items():
        if value != 0:
            agent_list.append(agent + str(value))

def init():
    '''
    for n in range(1,11):
        agent_list.append('ZI_Buy' + str(n))
        agent_list.append('ZI_Sell' + str(n))
    for n in range(1,3):
        agent_list.append('DT_Sell'+ str(n))
        agent_list.append('DT_Buy' + str(n))
    '''
    agent_list = []
    n = 1
    add_agents(n, agent_list)
    
    tick_num = 50
    api_connection = 'http://0.0.0.0:8000/'
    exp_name = 'exp'
    return agent_list, tick_num, api_connection, exp_name


if __name__ == '__main__':
    agent_list, tick_num, api_connection, exp_name = init()
    with DatabaseConnectionManager() as cursor:
        create_or_truncate_tables(cursor, exp_name)
    controller(agent_list, tick_num, api_connection, exp_name)
