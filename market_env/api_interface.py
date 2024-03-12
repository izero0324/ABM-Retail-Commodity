import requests

'''
Policy
'''

def post_order(Market: int, Price: int, Quantity: int, Name: str):

    url = 'http://0.0.0.0:8000/orders/'
    order_data = {
        "Market": Market,
        "Price" : Price,
        "Quantity" :  Quantity,
        "Side": "B" ,
        "Producer_name": Name
    }

    response = requests.post(url, json=order_data)

    if response.status_code == 200:
        print("Order posted successfully:", response.json())
    else:
        print("Failed to post order:", response.content)