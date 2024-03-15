import requests
from tools.sql_connection import DatabaseConnectionManager
def get_order_book(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Order book retrieved successfully.")
        return response.json()
    else:
        print("Failed to retrieve order book:", response.content)
        return []

def pairing(api_interface, tick_num, exp_name):
    url = api_interface + 'orders/'
    order_book = get_order_book(url)

    process_pairs(order_book,tick_num, exp_name)

def process_pairs(order_book, tick_num, exp_name):
    buy_orders = [order for order in order_book if order['Side'] == 'B']
    sell_orders = [order for order in order_book if order['Side'] == 'S']
    # Sort buy orders descending by price and quantity, sell orders ascending by price and descending by quantity
    buy_orders.sort(key=lambda x: (-x['Price'], -x['Quantity']))
    sell_orders.sort(key=lambda x: (x['Price'], -x['Quantity']))
    success_trades = []

    with DatabaseConnectionManager() as cursor:
        # Save original order book
        for order in order_book:
            cursor.execute(f"INSERT INTO OrderBook_{exp_name} (tick, agent_name, trade_price, quantity) VALUES (%s, %s, %s, %s)",
                           (tick_num, order['agent_name'], order['Price'], order['Quantity']))
    
        while buy_orders and sell_orders and buy_orders[0]['Price'] >= sell_orders[0]['Price']:
            highest_buy = buy_orders[0]
            lowest_sell = sell_orders[0]
            
            trade_quantity = min(highest_buy['Quantity'], lowest_sell['Quantity'])
            trade_price = lowest_sell['Price']  # The price at which the trade takes place can vary depending on your rules. Using the lowest sell price here.
            
            success_trades.append({'Buyer': highest_buy['agent_name'], 'Seller': lowest_sell['agent_name'], 'Quantity': trade_quantity, 'Price': trade_price})
            
            # Update quantities or remove orders as needed
            highest_buy['Quantity'] -= trade_quantity
            lowest_sell['Quantity'] -= trade_quantity

            if highest_buy['Quantity'] <= 0:
                buy_orders.pop(0)
            if lowest_sell['Quantity'] <= 0:
                sell_orders.pop(0)

            

        print("Success Trades:")
        for trade in success_trades:
            print(trade)
            cursor.execute(f"INSERT INTO SuccessTrade_{exp_name} (tick, buy_agent, sell_agent, trade_price, quantity) VALUES (%s, %s, %s, %s, %s)",
                           (tick_num, trade['Buyer'], trade['Seller'], trade['Price'], trade['Quantity']))
        
        # Record lowest and highest success trade prices
        lowest_price = min(trade['Price'] for trade in success_trades)
        highest_price = max(trade['Price'] for trade in success_trades)

        price_spread_sql = f"INSERT INTO PriceSpread_{exp_name} (tick, LowestSuccessTradePrice, HighestSuccessTradePrice) VALUES (%s, %s, %s)"
        cursor.execute(price_spread_sql, (tick_num, lowest_price, highest_price))
    
    

    
#pairing('http://0.0.0.0:8000/') #test pairing