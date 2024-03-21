import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
import pandas as pd


def update(frame, df, lines):
    '''
    Update function for animation, update data of line objects
    '''
    for line, column in zip(lines, [1, 2]):
        # Set data up to current frame (tick)
        line.set_data(df[0][:frame], df[column][:frame])
    return lines

def update_comparison(frame, df1, df2, lines):
    '''
    Update function for two dfs
    '''
    if frame < len(df1[0]):
        lines[0].set_data(df1[0][:frame], df1[1][:frame])  # DF1 Lowest
        lines[1].set_data(df1[0][:frame], df1[2][:frame])  # DF1 Highest
    if frame < len(df2[0]):
        lines[2].set_data(df2[0][:frame], df2[1][:frame])  # DF2 Lowest
        lines[3].set_data(df2[0][:frame], df2[2][:frame])  # DF2 Highest
    return lines

def plot_price_spread_dynamic(df, exp_name, save=False):
    '''
    Function to plot the animated price spread
    '''
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim((0, df[0].max())) 
    ax.set_ylim((min(df[1].min(), df[2].min())-1, max(df[1].max(), df[2].max())+1))  # Adjust y limits to data max
    
    lines = [plt.plot([], [], label='LowestSuccessTradePrice')[0],
             plt.plot([], [], label='HighestSuccessTradePrice')[0]]
    
    plt.title(f'Price Spread Over Ticks of {exp_name}')
    plt.xlabel('Tick')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    # Create animation
    anim = FuncAnimation(fig, update, frames=len(df[0])+1,interval=50, fargs=(df, lines), blit=True, repeat=False)
    if save: anim.save(f'PriceSpread_{exp_name}.mp4', fps=20, extra_args=['-vcodec', 'libx264'])
    plt.show()

def compare_price_spread_dynamic(df1, exp_name1, df2, exp_name2, save=False):
    '''
    Function to plot the animated comparism of two price spread
    '''
    fig, ax = plt.subplots(figsize=(10, 6)) 
    max_tick = max(df1[0].max(), df2[0].max())
    max_price = max(df1[1].max(), df1[2].max(), df2[1].max(), df2[2].max())
    min_price = min(df1[1].min(), df1[2].min(), df2[1].min(), df2[2].min())
    
    ax.set_xlim((0, max_tick)) 
    ax.set_ylim((min_price, max_price)) 
    
    lines = [plt.plot([], [], label=f'{exp_name1} LowestSuccessTradePrice')[0],
             plt.plot([], [], label=f'{exp_name1} HighestSuccessTradePrice')[0],
             plt.plot([], [], ':', label=f'{exp_name2} LowestSuccessTradePrice')[0],
             plt.plot([], [], ':', label=f'{exp_name2} HighestSuccessTradePrice')[0]]
    
    plt.title('Price Spread Comparison Over Ticks')
    plt.xlabel('Tick')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    # Create animation
    anim = FuncAnimation(fig, update_comparison, frames=max(len(df1[0]), len(df2[0])) + 1, fargs=(df1, df2, lines), blit=True, repeat=False)

    if save: 
        Writer = writers['ffmpeg']
        writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=1800, extra_args=['-vcodec', 'libx264'])
        anim.save(f'PriceSpread_{exp_name1}_{exp_name2}.mp4', writer)
    plt.show()


def plot_price_spread(df):
    '''
    Plotting the fixed price spread of a experiment
    '''
    plt.figure(figsize=(10, 6))
    plt.plot(df[0], df[1], label='LowestSuccessTradePrice', linestyle='-')
    plt.plot(df[0], df[2], label='HighestSuccessTradePrice', linestyle='-')
    
    plt.title('Price Spread Over Ticks')
    plt.xlabel('Tick')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_LossRatio(exp_name, LostRatio_ls, agents, agent_list):
    '''
    Plot the LossRatio of one agent
    Input:
    exp_name(str): experiment name, 
    LostRatio_ls(df): the loss ratio in list, 
    agents(str): agent, 
    agent_list(list): agent list 
    '''
    max_tick = range(0, len(LostRatio_ls))
    plt.plot(max_tick, LostRatio_ls, label='General')
    agent_index = 0
    for agent in agents:
        plt.plot(max_tick, agent, label=agent_list[agent_index])
        agent_index += 1

    plt.title(f'Efficient Ratio of {exp_name}')
    plt.xlabel('Ticks')
    plt.ylabel('Efficient Ratio')
    plt.legend()
    plt.show()

def plot_BS(Buy, Sell, exp_name):
    '''
    Plot buy/sell among all agents.
    '''
    ticks = range(0, max(len(Buy),len(Sell)))
    plt.plot(ticks, Buy, label='Buy')
    plt.plot(ticks, Sell, label='Sell')

    plt.title(f'Efficient Ratio of {exp_name}')
    plt.xlabel('Ticks')
    plt.ylabel('Efficient Ratio')
    plt.legend()
    plt.show()