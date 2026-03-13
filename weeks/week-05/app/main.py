from typing import List, Dict, Optional
from fastapi import FastAPI
from pydantic import BaseModel
import strawberry
from strawberry.fastapi import GraphQLRouter

app = FastAPI()


@strawberry.type
class Device:
    name: str
    serial: str
    id : int 


device_db: List[Device] = [
    Device(name="lobzik",serial="S1", id=1),
    Device(name="screbok",serial="S2", id=2),
]

next_id = len(device_db)+1


@strawberry.type
class Query:
    @strawberry.field
    def devices(self) -> List[Device]:
        return device_db

    @strawberry.field
    def device(self, id: int) -> Optional[Device]:
        for device in device_db:
            if device.id == id:
                return device
        return None
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_device(self, name: str, serial: str) -> Device:
        global next_id

        new_device = Device(
            id=next_id,
            name=name,
            serial=serial
        )
        device_db.append(new_device)
        next_id += 1
        return new_device

@app.get("/device", response_model=List[Device])
def get_a():
    return device_db


graphql_app = GraphQLRouter(strawberry.Schema(query=Query, mutation=Mutation))
app.include_router(graphql_app, prefix="/graphql")



