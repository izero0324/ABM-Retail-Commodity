import argparse
import json
import signal
import subprocess
import sys
import time

from tools.controller import controller
from tools.sql_connection import DatabaseConnectionManager, create_or_truncate_tables

def add_agents_from_config(agent_list, config_file='config.json'):
    '''
    Updates the agent list with agents from the config file.

    Input:
        agent_list: A list of current agents.
        config_file: The path to the configuration file.
    '''
    with open(config_file, 'r') as file:
        config = json.load(file)

    for agent, value in config['agents'].items():
        for n in range(value):
            agent_list.append(f"{agent}{n}")
    print(f"Agent_list: {agent_list}")

def exp_name_check(config_file='config.json'):
    '''avoid people don't change configs!'''
    args = parse_arguments()
    with open(config_file, 'r') as file:
        config = json.load(file)
        try:
            assert config['exp_name'] == args.exp_name
        except AssertionError:
            raise AssertionError('Check if you changed the config!')


def initialize_experiment(tick_num=50, exp_name='exp', api_connection='http://0.0.0.0:8000/'):
    '''
    Initializes the experiment with the necessary parameters.

    Input:
        tick_num: The number of ticks for the experiment.
        exp_name: The name of the experiment.
        api_connection: The API connection URL.

    Output:
        A tuple containing the list of agents, number of ticks, API connection URL, and experiment name.
    '''
    agent_list = []
    add_agents_from_config(agent_list)

    return agent_list, tick_num, api_connection, exp_name


def parse_arguments():
    '''
    Parses command-line arguments.

    Output:
        The parsed arguments.
    '''
    parser = argparse.ArgumentParser(description='Run an experiment with specified parameters.')
    parser.add_argument('--tick_num', type=int, default=50, help='Number of ticks.')
    parser.add_argument('--exp_name', type=str, default='exp', help='Experiment name.')
    parser.add_argument('--api_connection', type=str, default='http://0.0.0.0:8000/', help='API connection URL.')

    return parser.parse_args()

def main():
    '''
    Entry point
    '''
    args = parse_arguments()
    agent_list, tick_num, api_connection, exp_name = initialize_experiment(
        args.tick_num, args.exp_name, args.api_connection
    )
    
    sys.stdout = main_log # Store logs into log.txt from here

    with DatabaseConnectionManager() as cursor:
        create_or_truncate_tables(cursor, exp_name)
    
    controller(agent_list, tick_num, api_connection, exp_name, main_log)

def start_server(log):
    # Start uvicorn subprocess
    server_process = subprocess.Popen(['uvicorn', 'LOB_api:app', '--host', '0.0.0.0', '--port', '8000']
                                      ,stdout=background_log, stderr=background_log)
    return server_process

def stop_server(server_process):
    # Terminate the uvicorn subprocess
    server_process.terminate()
    server_process.wait()

if __name__ == '__main__':
    print("Experiment_name checking...")
    exp_name_check()

    print("Api server Starting ...")
    with open("log.txt", "w") as main_log, open("background_log.txt", "w") as background_log:
        server_process = start_server(background_log)
        time.sleep(1)
        print("Api server started! ")
        try:
            main_log.write("Main Process Start...\n")
            main()
            sys.stdout = sys.__stdout__ # Restart showing logs in terminal
            print("Simulation finished (Press CTRL+C to quit)")
            # Wait for KeyboardInterrupt (Ctrl+C) to stop the server
            signal.signal(signal.SIGINT, signal.default_int_handler)
            signal.pause()
        except KeyboardInterrupt:
            # Handle KeyboardInterrupt to stop the server gracefully
            stop_server(server_process)

    
