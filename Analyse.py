from analyse_tools.analyse_func import *
from analyse_tools.plot_price import *
import argparse
import sys
import signal

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

def main():
    '''
    Entry point
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


if __name__ == '__main__':
    #main()
    ratio = AllLossRatio("F2R_ZIP1")
    ratio_ls = AllLossRatioList("F2R_ZIP1")
    print(ratio)
    print(ratio_ls)
    print("Analyse finished (Press CTRL+C to quit)")
    

    