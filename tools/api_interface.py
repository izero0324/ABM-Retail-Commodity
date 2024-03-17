import requests

'''
Policy
'''
default_url = 'http://0.0.0.0:8000/'

def get_temp_order_book():
    url = default_url + 'orders/'
    response = requests.get(url)
    if response.status_code == 200:
        print("Order book retrieved successfully.")
        return response.json()
    else:
        print("Failed to retrieve order book:", response.content)
        return []

def post_order(Market: int, Price: float, Quantity: int, Name: str, side: str):
    '''
    Post an order to market.
    Input:
    market (int): Market identifier.
    price (float): Order price.
    quantity (int): Order quantity.
    name (str): Agent name.
    side (str): Order side ('buy' or 'sell').
    '''
    price = format(Price,'.2f')
    quantity = round(Quantity)
    if quantity <= 0:
        print("[API LOG]    Quantity is zero or negative. Order not posted.")
        return
    order_data = {
        "Market": Market,
        "Price" : price,
        "Quantity" :  quantity,
        "Side": side ,
        "agent_name": Name
    }
    response = requests.post(f'{default_url}orders/', json=order_data)

    if response.status_code == 200:
        print("[API LOG]    Order posted successfully:", response.json())
    else:
        print("[API ERROR]Failed to post order:", response.content)

def post_clear_order():
    url = default_url+'clear/'
    response = requests.post(url)

    if response.status_code == 200:
        print("[API LOG]    Order cleared successfully:", response.json())
    else:
        print("[API ERROR]Failed to post order:", response.content)

def get_agent_history(type:str, agent_name: str, n: int):
    '''
    Input:
    type: str #'order'/ 'trade'
    agent__name: str # agent_name
    n: int # day
    Output:
    dataframe of the specific agent on Trade/Order
    '''
    url = default_url+'hist/'+type+'/'+agent_name+'/'+str(n)
    response = requests.get(url)
    if response.status_code == 200:
        #print("[API LOG]    Hist get successfully!")
        return response.json()
    else:
        print("[API ERROR]Failed to post order:", response.content)
        return 0
    
def get_price_history(n: int):
    '''
    Input: 
    n: int # days
    Output:
    df: Price interval
    '''
    url = default_url+'hist/price/'+str(n)
    response = requests.get(url)
    if response.status_code == 200:
        print("[API LOG]    Hist get successfully!")
        return response.json()
    else:
        print("[API ERROR]Failed to get hist:", response.content)
        return 0
    
def get_trade_quant_list(n: int):
    url = default_url+'whole/quant/'+str(n)
    response = requests.get(url)
    if response.status_code == 200:
        print("[API LOG]    Last quant get successfully!")
        return response.json()
    else:
        print("[API ERROR]Failed to get quant:", response.content)
        return 0

def get_trade_price_list(n: int):
    url = default_url+'whole/price/'+str(n)
    response = requests.get(url)
    if response.status_code == 200:
        print("[API LOG]    Last price list get successfully!")
        return response.json()
    else:
        print("[API ERROR]Failed to get price list:", response.content)
        return 0

def get_order_book_after_pairing(n: int):
    url = default_url+'LOB/'+str(n)
    response = requests.get(url)
    if response.status_code == 200:
        print("[API LOG]    LOB get successfully!")
        return response.json()
    else:
        print("[API ERROR]Failed to get LOB:", response.content)
        return 0
