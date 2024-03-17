import numpy as np
from tools.api_interface import *

class functions:
    '''
    Functions used in strategies
    '''
    # Following code written by rowan
    def sign_func(self,S):
        '''
        Returns 1 if s is positive, else -1.
        '''
        return 1 if S > 0 else -1

    def current_price(self):
        '''
        Calculate the mean price of last tick from min_price and max_price
        Returns:
        float: The average (mean) price of the last trading period. If unable to obtain,
               it returns a default value of 13.5.
        '''
        try:
            One_hist_price = get_price_history(1) # Expected format: [[min_price, max_price]]
            # Collect yesterdayexecution price
            return(np.mean(One_hist_price[0]))
        except:
            return 13.5
        
    def price_trend(self):
        '''
        Determines the sign of the price trend over the last two days.
        Returns:
        int: Returns -1 for a negative trend, 1 for a positive trend.
        '''
        try:
            Two_hist_price = get_price_history(2)
            # Identify if the most recent price trend is positive or negative
            price_change = np.mean(Two_hist_price [1]) - np.mean(Two_hist_price [0])
            return(self.sign_func(price_change))
        except:
            # In case of any exception, default to a positive trend
            return 1
        
    def calculate_unexecuted_order_quantities(self, limit_order_book):
        # Calculate the quantity of all unexecuted order
        buy_quantity = sum(order[1] for order in limit_order_book if order[2] == "B")
        sell_quantity = sum(order[1] for order in limit_order_book if order[2] == "S")
        return buy_quantity, sell_quantity
    
    def quant_ratio(self):
        '''
        Ratio of quantities between buy and sell orders.
        Returns:
        list: [buy_quantity, sell_quantity, SellBuy_Ratio, BuySell_Ratio]
        '''
        limit_order_book = get_order_book_after_pairing(1)
        buy_quantity, sell_quantity = self.calculate_unexecuted_order_quantities(limit_order_book)
        try:
            BuySell_Ratio = buy_quantity / sell_quantity         # >1 is a good signal for seller
            SellBuy_Ratio = 1 / BuySell_Ratio          # >1 is a good signnal for buyer  
        except:
            # In case one of the quantity is 0, default to balance the ratio
            BuySell_Ratio= 1
            SellBuy_Ratio= 1
        return([buy_quantity, sell_quantity, SellBuy_Ratio, BuySell_Ratio])
    
    def trade_situation(self, agent_name, n):
        '''
        Evaluates trade situation based on agent's trade history.
        Input:
        agent_name (str): Name of the agent.
        n (int): Number of trade cycles to evaluate.
        Returns:
        int: -1 if no trades were made in all cycles, 1 otherwise.
        '''
        try:
            n_execuation = []
            for cycle in range(n):
                n_execuation_success = get_agent_history('trade', agent_name, cycle+1)
                n_execuation_total = get_agent_history('order', agent_name, cycle+1)
                traded = n_execuation_success[0][3:]
                total = float(n_execuation_total[-1][-1])
                result = traded.append(total)
                n_execuation.append(result)
            # Detect if the agent has not executed for more than n days
            for execution in n_execuation:
                if execution[0] > 0:
                    return 1
            return -1
        except:
            # In case there's no trades to be get, assume 1 for nutural
            return 1

    # The following was written by Viola:
    
    #Make strategies based on the trend of historical prices
    def analyze_trend(self, n):
        
######### Here's function need to be defined
        # The n days hitorical price intervals
        # Ten_hist_price = price_history(n) -> [ n days [min_deal_price,max_deal_price)] ]
        # Sample output
        '''
        Ten_hist_price = [[10.25,20.58], [14.5,12.77], [14.5,12.77], [14.5,12.77]
                          ,[14.5,12.77], [14.5,12.77], [14.5,12.77], [14.5,12.77]
                          ,[14.5,12.77], [14.5,12.77]]  
        '''
        n_day_hist_price  = get_price_history(n)
        
        # Calculate 10 days average price
        n_day_hist_average_price=[]
        for i in n_day_hist_price:
            n_day_hist_average_price.append(np.mean(i))
        # Analyze the trend of 10 days historical prices using linear regression 
        
        x = np.arange(n)
        slope, _ = np.polyfit(x, n_day_hist_average_price, 1)
        return slope
    
# The following was written by Jiaqi Xia:

    # Decide the market demand level according to the historical data
    def demand_level(self, n):
        market_demand_threshold_low = 50
        market_demand_threshold_high = 100
######### Here's function need to be defined
        # The n days hitorical execuation quantities
        # Ten_hist_exec_quant = exec_quant_history(n) -> [ n days execuation quantities ]
        # Sample output
        #Ten_hist_exec_quant = [15, 18, 19, 5, 25, 7, 15, 18, 0, 22] # get quant only
        n_hist_exec_quant = get_trade_quant_list(n)
        n_hist_exec_quant = [item for sublist in n_hist_exec_quant for item in sublist]

        average_sales = np.mean(n_hist_exec_quant)
        if average_sales < market_demand_threshold_low:
            demand_level = 'low'
        elif market_demand_threshold_low <= average_sales < market_demand_threshold_high:
            demand_level = 'medium'
        else:
            demand_level = 'high'
        return demand_level


# The following was wriiten by Jasmine:

######### Here's thing need to be defined
    # deal_sign = 0 , if there is no order executed yesterday
    # deal_sign = 1 , if order(s) were executed yesterday
    # Sample output
    def if_trade_yesterday():
        '''
        deal_sign = 0 , if there is no order executed yesterday
        deal_sign = 1 , if order(s) were executed yesterday
        Sample output
        '''
        trades = get_price_history(1)
        if len(trades) == 0:
            return 0 # deal_sign
        else:
            return 1 # deal_sign

        
    
    #Func_1 : competitor_price
    def competitor_price_history_f(self,agent_name):   
        if self.if_trade_yesterday(agent_name) == 0:
            
######### Here's function need to be defined
        # Latest limit order book, namely, limit order book after matching from yesterday 
        # limit_order_book = [ n lists [price, quantity,S/B]]
        # Sample output
            limit_order_book = get_order_book_after_pairing(1) # ADD WHOLE LOB
           
            competitor_price_history = [sublist[0] for sublist in limit_order_book if sublist[2] == "S"]
        else:
            
######### Here's function need to be defined
        # The n days hitorical price and quantity intervals
        # One_hist = history(n) -> [ n days [deal_1_price, deal_1_quantity] , [deal_2_price, deal_2_quantity] ]
        # Sample output
            One_hist = get_trade_price_list(1)
            competitor_price_history = [sublist[0] for sublist in One_hist] # Trade price list single tick n price [price, price, price]
            
        return competitor_price_history

    
    #Func_2 : buyer_price
    def buyer_price_willingness_history_f(self):
        if self.if_trade_yesterday() == 0:

        # Sample output
            limit_order_book = get_order_book_after_pairing(1)
            
            buyer_price_willingness_history = [sublist[0] for sublist in limit_order_book if sublist[2] == "B"]
        else:
            
       # Sample output
            One_hist = get_trade_price_list(1)
            buyer_price_willingness_history = [sublist[0] for sublist in One_hist] # trade price
             
        return buyer_price_willingness_history
 
    
    #Func_3 : buyer_order_quantity
    def buyer_order_quantities_f(self):
        if self.if_trade_yesterday() == 0:
            
        # Sample output
            limit_order_book = get_order_book_after_pairing(1)
            
            buyer_order_quantities = [sublist[1] for sublist in limit_order_book if sublist[2] == "B"]
        else:
            
        # Sample output
            One_hist = get_trade_price_list(1)
            buyer_order_quantities = [sublist[1] for sublist in One_hist] #Trade quantity list [quant1, quant2, .. qaunt10]
            
        return buyer_order_quantities
    

    #Func_4 : milk_production_quantity
    def production_quantity(mean_qty, std_dev):
        quantity = np.random.normal(mean_qty, std_dev)
        return quantity


    def buy_quantity(mean_qty, std_dev):
        quantity = np.random.normal(mean_qty, std_dev)
        return quantity


    
    
    
    
    
    
    
