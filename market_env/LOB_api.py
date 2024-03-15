from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid

app = FastAPI()

# Simulating NoSQL storage with in-memory dict.
orders_db = {}

class Order(BaseModel):
    Market: int # Market ID
    Price : int # Price
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
    return {"Next tick"}

# clear order book
@app.post("/clear/")
async def clear_all_orders():
    orders_db.clear()
    return {"Order list cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)