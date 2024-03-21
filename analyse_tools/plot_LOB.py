import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers

def plot_LOB_ani(data, save=False):
    '''
    Plot the Limit order book with animation!
    Input:
    data(df): A Whole limit order book in dataframe. Format: [Tick], [Price], [Quantity]
    save(bool): if True, save image.
    Output:
    matplot
    img
    '''
  
    num_ticks = data[0].max()  # Assuming ticks start at 0 and are sequential
    def animate(i):
        plt.cla()  # Clear current axes
        tick = i
        df_tick = data[data[0] == tick]
        
        buy_orders = df_tick[df_tick[3] == 'B'] # sort buy orders
        sell_orders = df_tick[df_tick[3] == 'S'] # sort sell orders
        max_qty = max(buy_orders[2].max(), sell_orders[2].max(), 1) 
        
        # Plotting
        plt.barh(buy_orders[1], buy_orders[2], color='green', label='Buy', left=0)
        plt.barh(sell_orders[1], -sell_orders[2], color='red', label='Sell', left=0)
        plt.xlabel('Quantity')
        plt.ylabel('Price')
        plt.title(f'Limit Order Book')
        plt.xlim(-max_qty, max_qty)  # Set x-axis center to 0
        ax.xaxis.set_visible(False)
        plt.legend(['Buy', 'Sell'], loc='upper right')

    fig, ax = plt.subplots() # show plot

    ani = FuncAnimation(fig, animate,interval=100, frames=num_ticks, repeat=False)
    if save:
        Writer = writers['ffmpeg']
        writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=1800, extra_args=['-vcodec', 'libx264'])
        ani.save(f'LOB.mp4', writer)
    plt.show()

def plot_order_book(tick, df):
    '''
    Plot single tick of the Limit order book!
    Input:
    tick(int): the tick numbrer of the limit order book
    data(df): A Whole limit order book in dataframe. Format: [Tick], [Price], [Quantity]
    Output:
    matplot
    '''
    df_tick = df[df[0]==tick]
    
    buy_orders = df_tick[df_tick[3] == 'B']#.sort_values(by=df_tick[1], ascending=True)
    sell_orders = df_tick[df_tick[3] == 'S']#.sort_values(by=df_tick[1], ascending=False)

    
    # Creating subplot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotting Buy orders
    ax.barh(buy_orders[1], buy_orders[2], color='green', label='Buy')
    # Plotting Sell orders
    ax.barh(sell_orders[1], -sell_orders[2], color='red', label='Sell')
    
    # Hide the X-axis line and ticks
    ax.xaxis.set_visible(False)
    
    # Manually set an X-axis label
    ax.set_xlabel('Quantity', labelpad=20)
    
    ax.set_ylabel('Price')
    ax.set_title(f'Limit Order Book at tick {tick}')
    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()

