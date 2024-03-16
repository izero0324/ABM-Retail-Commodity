import requests

'''
Policy
'''

def post_order(Market: int, Price: int, Quantity: int, Name: str, side: str):

    url = 'http://0.0.0.0:8000/orders/'
    order_data = {
        "Market": Market,
        "Price" : Price,
        "Quantity" :  Quantity,
        "Side": side ,
        "agent_name": Name
    }

    response = requests.post(url, json=order_data)

    if response.status_code == 200:
        print("Order posted successfully:", response.json())
    else:
        print("Failed to post order:", response.content)

def post_clear_order():
    url = 'http://0.0.0.0:8000/clear/'
    response = requests.post(url)

    if response.status_code == 200:
        print("Order cleared successfully:", response.json())
    else:
        print("Failed to post order:", response.content)

def get_agent_history(type:str, agent_name: str, n: int):
    '''
    Input:
    type: str #'order'/ 'trade'
    agent__name: str # agent_name
    n: int # day
    Output:
    dataframe of the specific agent on Trade/Order
    '''
    url = 'http://0.0.0.0:8000/hist/'+type+'/'+agent_name+'/'+n
    response = requests.get(url)
    if response.status_code == 200:
        print("Hist get successfully!")
        return response.json()
    else:
        print("Failed to post order:", response.content)
        return 0
    
def get_price_history(n: int):
    '''
    Input: 
    n: int # days
    Output:
    df: Price interval
    '''
    url = 'http://0.0.0.0:8000/hist/price/'+n
    response = requests.get(url)
    if response.status_code == 200:
        print("Hist get successfully!")
        return response.json()
    else:
        print("Failed to get hist:", response.content)
        return 0
    
def get_trade_quant_list(n: int):
    url = 'http://0.0.0.0:8000/whole/quant/'+n
    response = requests.get(url)
    if response.status_code == 200:
        print("Last quant get successfully!")
        return response.json()
    else:
        print("Failed to get quant:", response.content)
        return 0

def get_trade_price_list(n: int):
    url = 'http://0.0.0.0:8000/whole/price/'+n
    response = requests.get(url)
    if response.status_code == 200:
        print("Last price list get successfully!")
        return response.json()
    else:
        print("Failed to get price list:", response.content)
        return 0
