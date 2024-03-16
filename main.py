from tools.controller import controller
from tools.sql_connection import DatabaseConnectionManager, create_or_truncate_tables

def init():
    agent_list = []
    '''
    for n in range(1,11):
        agent_list.append('ZI_Buy' + str(n))
        agent_list.append('ZI_Sell' + str(n))
    for n in range(1,3):
        agent_list.append('DT_Sell'+ str(n))
        agent_list.append('DT_Buy' + str(n))
    '''
    n = 1
    agent_list.append('ZI_Buy' + str(n))
    agent_list.append('ZI_Sell' + str(n))
    agent_list.append('ZIP_Buy' + str(n))
    agent_list.append('ZIP_Sell' + str(n))
    agent_list.append('MD_Buy' + str(n))
    agent_list.append('MD_Sell' + str(n))
    agent_list.append('PN_Buy' + str(n))
    agent_list.append('PN_Sell' + str(n))
    agent_list.append('DT_Buy' + str(n))
    agent_list.append('DT_Sell' + str(n))
    agent_list.append('DYN_Sell' + str(n))
    
    tick_num = 50
    api_connection = 'http://0.0.0.0:8000/'
    exp_name = 'exp'
    return agent_list, tick_num, api_connection, exp_name


if __name__ == '__main__':
    agent_list, tick_num, api_connection, exp_name = init()
    with DatabaseConnectionManager() as cursor:
        create_or_truncate_tables(cursor, exp_name)
    controller(agent_list, tick_num, api_connection, exp_name)
