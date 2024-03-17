import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from tools.sql_connection import DatabaseConnectionManager

def update(frame, df, lines):
    # Update data of line objects
    for line, column in zip(lines, [1, 2]):
        # Set data up to current frame (tick)
        line.set_data(df[0][:frame], df[column][:frame])
    return lines

def plot_price_spread_dynamic(df, exp_name):
    # Set up the figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim((0, df[0].max()))  # Assuming 'df[0]' contains ticks
    ax.set_ylim((min(df[1].min(), df[2].min())-1, max(df[1].max(), df[2].max())+1))  # Adjust y limits to data max
    
    lines = [plt.plot([], [], label='LowestSuccessTradePrice')[0],
             plt.plot([], [], label='HighestSuccessTradePrice')[0]]
    
    plt.title(f'Price Spread Over Ticks of {exp_name}')
    plt.xlabel('Tick')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)

    # Create animation
    anim = FuncAnimation(fig, update, frames=len(df[0])+1, fargs=(df, lines), blit=True, repeat=False)
    #anim.save(f'pricespread_{exp_name}.mp4', fps=20, extra_args=['-vcodec', 'libx264'])

    plt.show()

def get_price_spread(exp_name):
    with DatabaseConnectionManager() as cursor:
        query = f"SELECT tick, LowestSuccessTradePrice, HighestSuccessTradePrice FROM PriceSpread_{exp_name} ORDER BY tick"
        cursor.execute(query)
        rows = cursor.fetchall()
        
    return pd.DataFrame(rows)


def plot_price_spread(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df[0], df[1], label='LowestSuccessTradePrice', linestyle='-')
    plt.plot(df[0], df[2], label='HighestSuccessTradePrice', linestyle='-')
    
    plt.title('Price Spread Over Ticks')
    plt.xlabel('Tick')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

