from analyse_tools.analyse_func import *
from analyse_tools.plot_price import *
from analyse_tools.plot_LOB import *
import argparse
import json


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
    return agent_list

def parse_arguments():
    '''
    Parses command-line arguments.

    Output:
        The parsed arguments.
    '''
    parser = argparse.ArgumentParser(description='Run analyse with specified parameters.')
    parser.add_argument('--compare', action="store_true", help='True for exp compare')
    parser.add_argument('--exp_name', type=str, default='exp', help='Experiment name.')
    parser.add_argument('--exp_name2', type=str, default='ZI_ZIP', help='Experiment name2.')
    parser.add_argument('--save', action="store_true", help='Call for storing mp4')

    return parser.parse_args()

def PriceSpread():
    '''
    Get PriceSpread 
    '''
    args = parse_arguments()
    exp_name = args.exp_name
    print(exp_name)
    price_spread_df = get_price_spread(exp_name)
    save_graph = False
    if args.save:
        save_graph = True
    if args.compare :
        exp_name2 = args.exp_name2
        price_spread_df2 = get_price_spread(exp_name2)
        compare_price_spread_dynamic(price_spread_df, exp_name, price_spread_df2, exp_name2, save_graph)
    else:
        print(price_spread_df)
        plot_price_spread_dynamic(price_spread_df, exp_name, save_graph)

def LossRatio_by_agent(agent_list):
    args = parse_arguments()
    exp_name = args.exp_name
    print(exp_name)
    LossRatio_df = AllLossRatioList(exp_name)
    all_agent_ER = []
    for agent in agent_list:
        all_agent_ER.append(AgentLossRatioList(exp_name, agent))
    plot_LossRatio(exp_name, LossRatio_df,  all_agent_ER, agent_list)

def LossRatio_BS():
    args = parse_arguments()
    exp_name = args.exp_name
    print(exp_name)
    LossRatio_df_B = AllLossRatioList(exp_name)
    LossRatio_df_S = AllLossRatioList(exp_name, side='Sell')
    plot_BS(LossRatio_df_B,  LossRatio_df_S, exp_name)

def limit_order_book_by_tick(tick):
    args = parse_arguments()
    exp_name = args.exp_name
    df = get_LOB(exp_name)
    # df[df[0]==tick]
    plot_order_book(tick, df)

def ani_LOB():
    args = parse_arguments()
    exp_name = args.exp_name
    df = get_LOB(exp_name)
    plot_LOB_ani(df, save=True)



if __name__ == '__main__':
    #agent_lists = ['ZI_Sell163', 'ZIP_Buy0', 'ZIP_Sell0']
    #agent_list = add_agents_from_config(agent_lists)
    #LossRatio_by_agent(agent_lists)
    #ratio = AllLossRatio("F2R_ZIP1")
    #ratio_ls = AllLossRatioList("F2R_ZIP1")
    ##print(ratio)
    #print(ratio_ls)
    #PriceSpread()
    ani_LOB()
    print("Analyse finished (Press CTRL+C to quit)")
    

    