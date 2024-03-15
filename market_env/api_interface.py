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