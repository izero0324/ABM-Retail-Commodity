import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from tools.get_history import *

app = FastAPI()

# Simulating NoSQL storage with in-memory dict.
orders_db = {}
exp_name = 'exp'

class Order(BaseModel):
    Market: int # Market ID
    Price : float # Price
    Quantity : int # n times base quantity
    Side: str #P for producer, B for buyer
    agent_name: str # agent_name

# post order
@app.post("/orders/")
async def create_order(order: Order):
    order_id = str(uuid.uuid4())
    orders_db[order_id] = order.dict()
    return {"order_id": order_id, **order.dict()}

# get one order
@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    order = orders_db.get(order_id)
    if order:
        return {"order_id": order_id, **order}
    raise HTTPException(status_code=404, detail="Order not found")

# get all orders
@app.get("/orders/", response_model=List[Order])
async def get_all_orders():
    return list(orders_db.values())

# next tick
@app.post("/next/")
async def next_step():
    clear_all_orders()
    return {"Next tick" }

# clear order book
@app.post("/clear/")
async def clear_all_orders():
    orders_db.clear()
    return {"Order list cleared"}

# Get history price
@app.get("/hist/price/{tick}")
async def get_history_price(tick:int):
    price_list = hist_n_price(exp_name, tick)
    return price_list

# Get history order by agent
@app.get("/hist/order/{agent}/{tick}")
async def get_history_order(agent:str, tick:int):
    order_list = hist_n_order_by_agent(exp_name,agent, tick)
    return order_list

# Get history trade by agent
@app.get("/hist/trade/{agent}/{tick}")
async def get_history_trade(agent:str, tick:int):
    trade_list = hist_n_trade_by_agent(exp_name,agent, tick)
    return trade_list

# Get trade_price list
@app.get("/whole/price/{tick}")
async def get_trade_price_list(tick: int):
    price_list = last_trade_price_list(exp_name, tick)
    return price_list

# Get n trade quantity
@app.get("/whole/quant/{tick}")
async def get_trade_quant_list(tick: int):
    quant_list = trade_quantity_list(exp_name, tick)
    return quant_list

# Get lob after pair
@app.get("/LOB/{tick}")
async def get_LOB(tick:int):
    lob = LOB_list(exp_name, tick)
    return lob

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)