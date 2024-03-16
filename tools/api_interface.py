import requests

'''
Policy
'''

def post_order(Market: int, Price: float, Quantity: int, Name: str, side: str):
    if type(Price) != float:
        Price = float(Price)
    if type(Quantity) != int:
        Quantity = round(Quantity)
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
        print("[API LOG] Order posted successfully:", response.json())
    else:
        print("[API ERROR]Failed to post order:", response.content)

def post_clear_order():
    url = 'http://0.0.0.0:8000/clear/'
    response = requests.post(url)

    if response.status_code == 200:
        print("[API LOG] Order cleared successfully:", response.json())
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
    url = 'http://0.0.0.0:8000/hist/'+type+'/'+agent_name+'/'+str(n)
    response = requests.get(url)
    if response.status_code == 200:
        print("[API LOG] Hist get successfully!")
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
    url = 'http://0.0.0.0:8000/hist/price/'+str(n)
    response = requests.get(url)
    if response.status_code == 200:
        print("[API LOG] Hist get successfully!")
        return response.json()
    else:
        print("[API ERROR]Failed to get hist:", response.content)
        return 0
    
def get_trade_quant_list(n: int):
    url = 'http://0.0.0.0:8000/whole/quant/'+str(n)
    response = requests.get(url)
    if response.status_code == 200:
        print("[API LOG] Last quant get successfully!")
        return response.json()
    else:
        print("[API ERROR]Failed to get quant:", response.content)
        return 0

def get_trade_price_list(n: int):
    url = 'http://0.0.0.0:8000/whole/price/'+str(n)
    response = requests.get(url)
    if response.status_code == 200:
        print("[API LOG] Last price list get successfully!")
        return response.json()
    else:
        print("[API ERROR]Failed to get price list:", response.content)
        return 0

def get_order_book_after_pairing(n: int):
    url = 'http://0.0.0.0:8000/LOB/'+str(n)
    response = requests.get(url)
    if response.status_code == 200:
        print("[API LOG] LOB get successfully!")
        return response.json()
    else:
        print("[API ERROR]Failed to get LOB:", response.content)
        return 0
