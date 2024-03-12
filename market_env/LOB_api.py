from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid

app = FastAPI()

# Simulating NoSQL storage with in-memory dict.
orders_db = {}

class Order(BaseModel):
    type: str  # "buy" or "sell"
    price: float
    quantity: int
    asset: str

@app.post("/orders/")
async def create_order(order: Order):
    order_id = str(uuid.uuid4())
    orders_db[order_id] = order.dict()
    return {"order_id": order_id, **order.dict()}

@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    order = orders_db.get(order_id)
    if order:
        return {"order_id": order_id, **order}
    raise HTTPException(status_code=404, detail="Order not found")

@app.get("/orders/", response_model=List[Order])
async def get_all_orders():
    return list(orders_db.values())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)