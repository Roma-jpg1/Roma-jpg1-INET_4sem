from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Comment(BaseModel):
    id: int
    author: str
    email: str

class CreateComment(BaseModel):
    author: str
    email: str
    


# В этом месте вам необходимо реализовать REST API согласно варианту

#переделать на список -----------------------------
comments_db: List[Comment] = [
    Comment(id=1, author="Alice", email="test@mail.com"),
    Comment(id=2, author="Bob", email="hello@imbob.com"),
]

next = len(comments_db)+1

@app.get("/health", response_model=Dict[str, str])
def get_health():
    return {"status": "ok"}

@app.get("/emails", response_model=List[Comment])
def get_a():
    return comments_db



@app.post("/emails", response_model=Comment)
def post(comment: CreateComment):
    global next
    new_comment = Comment(id=next, author=comment.author, email=comment.email)
    comments_db.append(new_comment)
    next += 1
    return new_comment


@app.get("/emails/{id}", response_model=Comment)
def get_ms(mes_id: int):
    for m in comments_db:
        if m.id == mes_id:
            return m 