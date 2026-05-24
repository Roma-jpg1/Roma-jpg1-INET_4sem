from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import grpc

import likes_pb2
import likes_pb2_grpc

from .db import SessionLocal, engine, Base
from .models import Post

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Post Service API", description="API for managing posts")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

@app.post("/posts")
def create_post(title: str, content: str, db: Session = Depends(get_db)):
    new_post = Post(title=title, content=content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{post_id}") # доделать grpc
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return {"message": f"Post with id {post_id} deleted"}
    else:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")