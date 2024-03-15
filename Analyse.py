from analyse_tools.price_spread import *

exp_name = 'exp'
if __name__ == '__main__':
    price_spread_df = get_price_spread(exp_name)
    print(price_spread_df)
    plot_price_spread(price_spread_df)