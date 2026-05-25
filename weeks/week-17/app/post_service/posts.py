from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import grpc

from db import SessionLocal, engine, Base
from models import Post

from proto import likes_pb2
from proto import likes_pb2_grpc

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Post Service API", description="API for managing posts")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"database is unavailable: {e}")
    return {"status": "ok", "service": "post-service"}



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

@app.get("/posts/{post_id}")
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):

    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Post with id {post_id} not found"
        )

    try:

        channel = grpc.insecure_channel(
            "like-service:50051"
        )

        stub = (
            likes_pb2_grpc
            .LikeServiceStub(channel)
        )

        response = stub.GetLikesCount(
            likes_pb2.LikeRequest(
                post_id=post_id
            )
        )

        likes_count = response.count

    except Exception as e:

        print("gRPC ERROR:", e)

        likes_count = 0

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "likes_count": likes_count
    }
    

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return {"message": f"Post with id {post_id} deleted"}
    else:
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
