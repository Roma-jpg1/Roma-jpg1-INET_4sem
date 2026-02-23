from typing import List, Dict
from fastapi import FastAPI

app = FastAPI()

class message:
    id: int
    text: str
    topic: str

class CreateMessage:
    text: str
    topic: str
    


# В этом месте вам необходимо реализовать REST API согласно варианту

#переделать на список -----------------------------
message_db: Dict[int, message] = { 
    1: message(id=1, text="Hello", topic="study"),
    2: message(id=2, text="FastAPI is cool", topic="python"),
}

next = len(message_db)+1

@app.get("/messages", resp_model=List[message])
def get_a():
    return [message_db[k] for k in sorted(message_db.keys())]



@app.post("/messages", resp_model=message)
def post(ms: CreateMessage):
    global next
    message_db.append(ms)
    next+=1
    return ms


@app.get("/message/{id}", response_model=message)
def get_ms(mes_id: int):
    for m in message_db:
        if m.id == mes_id:
            return m 