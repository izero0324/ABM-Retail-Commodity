from analyse_tools.price_spread import *
import argparse
import subprocess
import time
import sys
import signal

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
    plot_price_spread_dynamic(price_spread_df, exp_name)

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
    print("Api server Starting ...")
    with open("an_log.txt", "w") as main_log, open("an_background_log.txt", "w") as background_log:
        server_process = start_server(background_log)
        time.sleep(1)
        print("Api server started! ")
        try:
            main_log.write("Main Process Start...\n")
            main()
            sys.stdout = sys.__stdout__ # Restart showing logs in terminal
            print("Analyse finished (Press CTRL+C to quit)")
            # Wait for KeyboardInterrupt (Ctrl+C) to stop the server
            signal.signal(signal.SIGINT, signal.default_int_handler)
            signal.pause()
        except KeyboardInterrupt:
            # Handle KeyboardInterrupt to stop the server gracefully
            stop_server(server_process)
    