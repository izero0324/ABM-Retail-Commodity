import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_LOB_ani(data):
    # Assuming the DataFrame 'data' is already defined and loaded with the Limit Order Book info
    # Modify this plotting function for animation
    def animate(i):
        plt.cla()  # Clear current axes to avoid overlaying plots
        tick = i
        df_tick = data[data[0] == tick]
        
        if df_tick.empty:
            plt.gca().axis('off')  # Hide axes for empty frames
            return
        
        buy_orders = df_tick[df_tick[3] == 'B']#.sort_values(by='price', ascending=True)
        sell_orders = df_tick[df_tick[3] == 'S']#.sort_values(by='price', ascending=False)
        max_qty = max(buy_orders[2].max(), sell_orders[2].max(), 1) 
        
        # Plotting
        plt.barh(buy_orders[1], buy_orders[2], color='green', label='Buy', left=0)
        plt.barh(sell_orders[1], -sell_orders[2], color='red', label='Sell', left=0)
        plt.xlabel('Quantity')
        plt.ylabel('Price')
        plt.title(f'Limit Order Book at tick {tick}')
        plt.xlim(-max_qty, max_qty)  # Set x-axis to center at 0
        ax.xaxis.set_visible(False)
        # We choose not to display the axes in this version as per earlier request, but you can adjust as needed
        plt.legend(['Buy', 'Sell'], loc='upper right')

    fig, ax = plt.subplots()

    # Assuming ticks are sequential and start from 0, adjust as necessary
    num_ticks = data[0].max()  # Assuming ticks start at 0 and are sequential
    ani = FuncAnimation(fig, animate,interval=100, frames=num_ticks, repeat=False)

    plt.show()

def plot_order_book(tick, df):
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

