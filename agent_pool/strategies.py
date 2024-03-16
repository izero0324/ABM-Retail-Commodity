from agent_pool.strategy_functions import functions 
import numpy as np


# The following was written by Jhao-Wei Chen:

# A strategy set used by agents


# A strategy set used by agents
class Strategies:
    #Quantity constraint
    Max_bid_quantity = 200
    Min_ask_quantity = 100
    Bid_q_mean = 100
    Bid_q_std_dev = 10
    Ask_q_mean = 150
    Ask_q_std_dev = 12
    
    #Price constraint
    Max_bid_price = 20.5
    Min_ask_price =23.4
    Bid_p_mean = 120
    Bid_p_std_dev = 13
    Ask_p_mean = 150
    Ask_p_std_dev = 10
    
    # ID: agents name, Side: B / S
    def init(self, ID, Side):
        self.ID = ID
        self.Side = Side


        
    # Zero intellengence strategy
    def ZI(self):
        if self.Side == "B":
            p = np.random.normal(self.Bid_p_mean, self.Bid_p_std_dev)
            q = round(np.random.normal(self.Bid_q_mean, self.Bid_q_std_dev))
        else:
            p = np.random.normal(self.Ask_p_mean, self.Ask_p_std_dev)
            q = round(np.random.normal(self.Ask_q_mean, self.Ask_q_std_dev))
        return (self.Side, p, q )
    
    def dynamic_pricing_strategy(self):
        # Dynamic pricing strategy: adjust the price and quantity according to the market demend level
        n = 10
        if self.Side == "B":
            if functions().demand_level(n) == 'high':
                price = min(functions().current_price() * 0.8, self.Max_bid_price)
                quantity = min(self.Max_bid_quantity * 0.2, self.Max_bid_quantity)
            elif functions().demand_level(n) == 'medium':
                price = functions().current_price() * 0.5
                quantity = self.Max_bid_quantity 
            else:
                price = min(functions().current_price() * 0.2, self.Max_bid_price)
                quantity = min(self.Max_bid_quantity * 0.8, self.Max_bid_quantity) 
        else:
            if functions().demand_level(n) == 'high':
                price = max(functions().current_price() * 0.8, self.Min_ask_price)
                quantity = max(self.Min_ask_quantity * 0.2, self.Min_ask_quantity)
            elif functions().demand_level == 'medium':
                price = functions().current_price()  * 0.5
                quantity = self.Min_ask_quantity  
            else:
                price = max(functions().current_price() * 0.2, self.Min_ask_price)
                quantity = max(self.Min_ask_quantity * 0.8, self.Min_ask_quantity) 
        return (self.Side, price, quantity)
    
    # Zero intellengence plus strategy
    def ZIP(self,GreedyLevel): # GreedyLevel from 0 to 1000 

        # Get 4 parameters
        Current_Price = functions().current_price() # pounds
        Trend_Sign = functions().price_trend() # +1 or -1
        Quant_Ratio = functions().quant_ratio() # first element for buyer, second for seller
        Trade_Situation = functions().trade_situation(self.ID, 3) # +1 or -1
        
        # Classify thhe agent's side and mix 4 parameters
        if self.Side == "B":
            # Convert parameters into factors
            Trend_Sign_factor =  1 + 0.1*Trend_Sign
            Quant_Ratio_factor = 1 + 0.1 * (Quant_Ratio[2] - 1)
            Trade_Situation_factor = -0.2 + abs(Trade_Situation+0.2) 
            p = Current_Price * Trend_Sign_factor * Quant_Ratio_factor * Trade_Situation_factor
            p = min(p,self.Max_bid_price)
            q = GreedyLevel * Quant_Ratio[1]
            q = min(q,self.Max_bid_quantity)
        else:
            # Convert parameters into factors
            Trend_Sign_factor =  1 + 0.1*Trend_Sign
            Quant_Ratio_factor = 1 + 0.1 * (Quant_Ratio[3] - 1)
            Trade_Situation_factor = 0.2 + abs(Trade_Situation-0.2) 
            p = Current_Price * Trend_Sign_factor * Quant_Ratio_factor * Trade_Situation_factor
            p = max(p,self.Min_ask_price)
            q = GreedyLevel * Quant_Ratio[0]
            q = max(q,self.Min_ask_quantity)
        
        return(self.Side,p,q)
    
    def penetration(self):
        if self.Side == 'S':
            # Estimating the lowest acceptable price based on buyer's willingness and competitor's pricing
            target_price_based_on_buyers = max(functions().buyer_price_willingness_history_f()) - 0.01
            target_price_based_on_sellers = min(functions().competitor_price_history_f())
    
            # Choosing the higher price between the target prices while ensuring it's above cost
            proposed_price = max(target_price_based_on_buyers, target_price_based_on_sellers, Strategies.Min_ask_price)
            quantity = round(functions.production_quantity(Strategies.Ask_q_mean, Strategies.Ask_q_std_dev))
        else:
            target_price_based_on_buyers = max(functions().buyer_price_willingness_history_f()) + 0.01
            target_price_based_on_sellers = min(functions().competitor_price_history_f())
            
            # Choosing the higher price between the target prices while ensuring it's above cost
            proposed_price = min(target_price_based_on_buyers, target_price_based_on_sellers, Strategies.Max_bid_price)
            quantity = round(functions.buy_quantity(Strategies.Bid_q_mean, Strategies.Bid_q_std_dev))

        return (self.Side, proposed_price, quantity)
    
    def dynamic(self):
        
        # Analyze market trends based on historical data
        avg_sellers_price = np.mean(functions().competitor_price_history_f())
        weighted_avg_buyer_price = np.average(functions().competitor_price_history_f(), weights=functions().buyer_order_quantities_f())
        
        if self.Side == 'S':
            # Strategy: Set price slightly below the average competitor's price but not lower than weighted average buyer price
            proposed_price = min(avg_sellers_price, weighted_avg_buyer_price) - 0.01
            # Ensure proposed price is above cost plus minimum margin
            proposed_price = max(proposed_price, self.Min_ask_price)
            quantity = round(self.Min_ask_quantity)                  
            
        return ('S', proposed_price, quantity)
    
    def decide_order_trend_strategy(self):
        n = 10 # Past 10 trades
        trend = functions().analyze_trend(n)
        # Classify the agent's side
        if self.Side == "B":
            quantity = functions.buy_quantity(self.Bid_q_mean, self.Bid_q_std_dev)
            if trend < 0: 
            #If price is decreasing, the buyer will lower the price at the speed of the trend.
                expected_price = min(functions().current_price() * (1 + trend), self.Max_bid_price)
            else:
            #If the price is stable or increasing, the buyer will keep the current price
                expected_price = min(functions().current_price(), self.Max_bid_price)
        
        else:
            quantity = functions.production_quantity(self.Ask_q_mean, self.Ask_q_std_dev)
            if trend > 0:
            #If price is increasing, the producer will higher the price at the speed of the trend.
                expected_price = max(functions().current_price() * (1 + trend), self.Min_ask_price)
            else:
            #If the price is stable or decreasing, the buyer will keep the current price
                expected_price = max(functions().current_price(), self.Min_ask_price)
        
        return (self.Side, expected_price, quantity)