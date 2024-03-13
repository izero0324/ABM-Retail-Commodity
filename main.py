from tools.controller import controller

def init():
    agent_list = ('agent1', 'agent2')
    tick_num = 2
    api_connection = 'http://0.0.0.0:8000/'
    return agent_list, tick_num, api_connection


if __name__ == '__main__':
    controller(init())
