from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Comment(BaseModel):
    id: int
    author: str
    text: str

class CreateComment(BaseModel):
    author: str
    text: str
    


# В этом месте вам необходимо реализовать REST API согласно варианту

#переделать на список -----------------------------
comments_db: List[Comment] = [
    Comment(id=1, author="Alice", text="hello im alice"),
    Comment(id=2, author="Bob", text="hello im bob"),
]

next = len(comments_db)+1

@app.get("/comments", response_model=List[Comment])
def get_a():
    return comments_db



@app.post("/comments", response_model=Comment)
def post(comment: CreateComment):
    global next
    new_comment = Comment(id=next, author=comment.author)
    comments_db.append(new_comment)
    next += 1
    return new_comment


@app.get("/comments/{id}", response_model=Comment)
def get_ms(mes_id: int):
    for m in comments_db:
        if m.id == mes_id:
            return m 