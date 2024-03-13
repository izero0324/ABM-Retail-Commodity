import requests

def get_order_book(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Order book retrieved successfully.")
        return response.json()
    else:
        print("Failed to retrieve order book:", response.content)
        return []

def pairing(api_interface):
    url = api_interface + 'orders/'
    order_book = get_order_book(url)
    process_pairs(order_book)

def process_pairs(order_book):
    buy_orders = [order for order in order_book if order['Side'] == 'B']
    sell_orders = [order for order in order_book if order['Side'] == 'S']
    # Sort buy orders descending by price and quantity, sell orders ascending by price and descending by quantity
    buy_orders.sort(key=lambda x: (-x['Price'], -x['Quantity']))
    sell_orders.sort(key=lambda x: (x['Price'], -x['Quantity']))
    success_trades = []
    
    while buy_orders and sell_orders and buy_orders[0]['Price'] >= sell_orders[0]['Price']:
        highest_buy = buy_orders[0]
        lowest_sell = sell_orders[0]
        
        trade_quantity = min(highest_buy['Quantity'], lowest_sell['Quantity'])
        trade_price = lowest_sell['Price']  # The price at which the trade takes place can vary depending on your rules. Using the lowest sell price here.
        
        success_trades.append({'Buyer': highest_buy['Producer_name'], 'Seller': lowest_sell['Producer_name'], 'Quantity': trade_quantity, 'Price': trade_price})
        
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

    
#pairing('http://0.0.0.0:8000/') #test pairing