from analyse_tools.price_spread import *
import argparse
import subprocess
import time
import sys

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
    print("Api server Starting ...")
    with open("log.txt", "w") as main_log, open("background_log.txt", "w") as background_log:
        subprocess.Popen(['python3', 'LOB_api.py'], stdout=background_log, stderr=background_log)
        time.sleep(3)
        print("Api server started!")
        sys.stdout = main_log
        main_log.write("Main Process Start...\n")
        main()
    sys.stdout = sys.__stdout__
    print("Simulation finished")
    