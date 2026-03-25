from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Shipment(BaseModel):
    id: int
    tracking: str

class CreateShipment(BaseModel):
    tracking: str
    


# В этом месте вам необходимо реализовать REST API согласно варианту

#переделать на список -----------------------------
shipment_db: List[Shipment] = [
    Shipment(id=1, tracking="122 122"),
    Shipment(id=2, tracking="42 23"),
]

next = len(shipment_db)+1

@app.get("/shipment", response_model=List[Shipment])
def get_a():
    return shipment_db



@app.post("/shipment", response_model=Shipment)
def post():
    global next
    new_ship = Shipment(id=next, tracking="ship")
    shipment_db.append(new_ship)
    next += 1
    return new_ship