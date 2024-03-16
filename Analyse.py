from analyse_tools.price_spread import *
import argparse


def parse_arguments():
    '''
    Parses command-line arguments.

    Output:
        The parsed arguments.
    '''
    parser = argparse.ArgumentParser(description='Run analyse with specified parameters.')
    parser.add_argument('--exp_name', type=str, default='exp', help='Experiment name.')
    return parser.parse_args()

def main():
    '''
    Entry point
    '''
    args = parse_arguments()
    exp_name = args.exp_name
    price_spread_df = get_price_spread(exp_name)
    print(price_spread_df)
    plot_price_spread(price_spread_df)

if __name__ == '__main__':
    main()
    