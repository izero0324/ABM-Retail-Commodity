# Start server
`python3 LOB_api.py` -> this will start a local api server  by uvicorn

# Post orders
curl -X 'POST' 'http://0.0.0.0:8000/orders/' -H 'accept: application/json'  -H 'Content-Type: application/json' 
  -d '{
    "Market": 1,
    "Price" : 100,
    "Quantity" :  10,
    "Side": "B" ,
    "Producer_name": "B00001"
}

# LOB
tick | Order1 | Order2 | ... | Order n
---
1    |  (Price, Volumn, side) | 

# Self record
tick | Agent1 | Agent 2 | Agent 3
---
1    | [Price, Amount, total_amount]