import argparse
import json

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
        if value != 0:
            agent_list.append(f"{agent}{value}")


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

    with DatabaseConnectionManager() as cursor:
        create_or_truncate_tables(cursor, exp_name)

    controller(agent_list, tick_num, api_connection, exp_name)


if __name__ == '__main__':
    main()
