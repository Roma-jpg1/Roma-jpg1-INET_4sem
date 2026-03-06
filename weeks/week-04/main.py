from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.saga import SagaOrch, SagaStep

app = FastAPI()

class Review(BaseModel):
    id: int
    author: str
    text: str
    rating: int

class CreateReview(BaseModel):
    author: str
    text: str
    rating: int

reviews_db: List[Review] = [
    Review(id=1, author="Alice", text="hello im alice", rating=3),
    Review(id=2, author="Bob", text="hello im bob", rating=5),
]

index_ids =[]

next_id = len(reviews_db) + 1

@app.get("/reviews", response_model=List[Review])
def list_reviews():
    return reviews_db

@app.post("/reviews", response_model=Review, status_code=201)
def create_review(re: CreateReview):
    global next_id
    cr=None

    def s1():
        nonlocal cr
        global next_id
        cr = Review(id=next_id, author=re.author, text=re.text, rating=re.rating)
        reviews_db.append(cr)
        next_id+=1
    def s1_comp():
        if cr in reviews_db:
            reviews_db.remove(cr)

    def s2():
        if cr.rating<1 or cr.rating>5:
            raise Exception("Invalid rating")
    def s2_comp():
        pass
    
    def s3():
        index_ids.append(cr.id)

    def s3_comp():
        if cr.id in index_ids:
            index_ids.remove(cr.id)


    saga = SagaOrch([
        SagaStep("save_review", s1, s1_comp, "STEP1_OK"),
        SagaStep("validate_review", s2, s2_comp, "STEP2_OK"),
        SagaStep("index_review", s3, s3_comp, "STEP3_OK"),
    ])

    try:
        saga.run()
    except Exception:
        raise HTTPException(status_code=409, detail="Saga failed")

    return cr

@app.get("/reviews/{review_id}", response_model=Review)
def get_review(review_id: int):
    for r in reviews_db:
        if r.id == review_id:
            return r
    raise HTTPException(status_code=404, detail="Review not found")