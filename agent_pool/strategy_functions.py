import numpy as np
from tools.api_interface import *

class functions:
    '''
    Functions used in strategies
    '''
    default_current_price = 13.5 #by rowan
    default_price_trend = 1      #by rowan
    default_quant_ratio = 1      #by rowan
    default_trade_situation = 1  #by rowan
    default_analyze_slope = 0    #by viola
    default_current_quantity =4.5#by jasmine

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
        except Exception as e:
            # In case the history isn't available return default price
            print(f"[Warning]    An error occurred: {e}") 
            print(f"[Warning]    Return default price: ",self.default_current_price)
            return self.default_current_price
        
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
        except Exception as e:
            # In case of any exception, default to a positive trend
            print(f"[Warning]    An error occurred: {e}") 
            print(f"[Warning]    Return default trend: ",self.default_price_trend)
            return self.default_price_trend
        
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
        except Exception as e:
            # In case one of the quantity is 0, default to balance the ratio
            print(f"[Warning]    An error occurred: {e}") 
            print(f"[Warning]    Return default quant_ratio: ",self.default_quant_ratio)
            BuySell_Ratio= self.default_quant_ratio
            SellBuy_Ratio= self.default_quant_ratio
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
        except Exception as e:
            print(f"[Warning]    An error occurred: {e}") 
            print(f"[Warning]    Return default trade_situation: ",self.default_trade_situation)
            # In case there's no trades to be get, assume 1 for nutural
            return self.default_trade_situation

    # The following was written by Viola:
    def analyze_trend(self, n):
        '''
        For strategies based on the trend of historical prices.
        Calculate n days average price from historical prices,
        and analyze the trend using linear regression.
        Input:
        n: int # n-days 
        Return:
        slope: float #The slope of the average price
        '''
        try:
            n_day_hist_price  = get_price_history(n)
            average_prices = [np.mean(day_prices) for day_prices in n_day_hist_price]
            days = np.arange(n)
            slope, _ = np.polyfit(days, average_prices, 1)
        except Exception as e:
            print(f"[Warning]    An error occurred: {e}") 
            print(f"[Warning]    Return default slope: ",self.default_analyze_slope)
            slope = self.default_analyze_slope

        return slope
    
    # The following was written by Jiaqi Xia:
    def demand_level(self, n):
        '''
        Determines the demand level based on the average trading quantities over the past n days.
        Input:
        n: The number of days to look back
        Returns:
        demand level ('low', 'medium', or 'high')
        '''
        market_demand_threshold_low = 50
        market_demand_threshold_high = 100    
        try:
            n_hist_exec_quant = get_trade_quant_list(n)
            flat_list = [item for sublist in n_hist_exec_quant for item in sublist]
            if not flat_list:
                print("[Warning]    No History")
                print("[Warning]    Return default demand: 'medium'")
                return 'medium'
            average_sales = np.mean(flat_list)
            if average_sales < market_demand_threshold_low:
                return 'low'
            elif market_demand_threshold_low <= average_sales < market_demand_threshold_high:
                return 'medium'
            else:
                return 'high'
        except Exception as e:
            print(f"[Warning]    An error occurred: {e}") 
            print("[Warning]    Return default demand: 'medium'")
            return 'medium'

    # The following was wriiten by Jasmine:
    def if_trade_yesterday():
        '''
        deal_sign = 0 , if there is no order executed yesterday
        deal_sign = 1 , if order(s) were executed yesterday
        Sample output
        '''
        trades = get_price_history(1)
        return 1 if trades else 0
    
    def get_competitor_price_history(self,agent_name):
        '''
        If failed to trade yesterday, get competitor price as price.
        Input:
        agent_name(str): agent
        Return:
        Price_list(list)
        ''' 
        try:
            if self.if_trade_yesterday(agent_name) == 0:
                limit_order_book = get_order_book_after_pairing(1) # ADD WHOLE LOB
                competitor_price_history = [sublist[0] for sublist in limit_order_book if sublist[2] == "S"]
                return competitor_price_history
            else:
                One_hist = get_trade_price_list(1)
                # Trade price list single tick n price [price, price, price]
                trade_price_history = [sublist[0] for sublist in One_hist] 
                return trade_price_history
        except Exception as e:
            print(f"[Warning]    An error occurred: {e}") 
            print(f"[Warning]    Return default price: {self.default_current_price}")
            return [self.default_current_price]

    def get_buyer_willingness_price_history(self):
        '''
        Get the buyer's bid price. Raise the price if traded, else be sure to trade
        Return:
        Price_list(list) : Default price if no history found
        '''
        try:
            if self.if_trade_yesterday() == 0:
                limit_order_book = get_order_book_after_pairing(1)
                buyer_price_willingness_history = [sublist[0] for sublist in limit_order_book if sublist[2] == "B"]
            else:
                One_hist = get_trade_price_list(1)
                # Trade price list single tick n price [price, price, price]
                buyer_price_willingness_history = [sublist[0] for sublist in One_hist]
            return buyer_price_willingness_history
        except Exception as e:
            print(f"[Warning]    An error occurred: {e}") 
            print(f"[Warning]    Return default price: {self.default_current_price}")
            return [self.default_current_price]
 
    def get_buyer_order_quantities(self):
        '''
        Get buyer's willing quantity
        Return:
        quantity(list): Default if no history.
        '''
        try:
            if self.if_trade_yesterday() == 0:
                limit_order_book = get_order_book_after_pairing(1)
                buyer_order_quantities = [sublist[1] for sublist in limit_order_book if sublist[2] == "B"]
            else:
                One_hist = get_trade_price_list(1)
                #Trade quantity list [quant1, quant2, .. qaunt10]
                buyer_order_quantities = [sublist[1] for sublist in One_hist] 
            return buyer_order_quantities
        except Exception as e:
            print(f"[Warning]    An error occurred: {e}") 
            print(f"[Warning]    Return default quantity: {self.default_current_quantity}")
            return [self.default_current_quantity]
    
    def production_quantity(mean_qty, std_dev):
        '''Generate a production quantity based on a normal distribution.'''
        quantity = np.random.normal(mean_qty, std_dev)
        return quantity


    def buy_quantity(mean_qty, std_dev):
        '''Generate a buying quantity based on a normal distribution.'''
        quantity = np.random.normal(mean_qty, std_dev)
        return quantity


    
    
    
    
    
    
    
