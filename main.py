from tools.controller import controller
from tools.sql_connection import MySQLConnectionManager, create_or_truncate_tables

def init():
    agent_list = []
    for n in range(20):
        agent_list.append('agent' + str(n))
    tick_num = 50
    api_connection = 'http://0.0.0.0:8000/'
    exp_name = 'exp'
    return agent_list, tick_num, api_connection, exp_name


if __name__ == '__main__':
    agent_list, tick_num, api_connection, exp_name = init()
    with MySQLConnectionManager() as cursor:
        create_or_truncate_tables(cursor, exp_name)
    controller(agent_list, tick_num, api_connection, exp_name)
