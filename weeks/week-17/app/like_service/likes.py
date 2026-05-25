from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import SessionLocal, engine, Base
from models import Like
import threading
from grpc_server import start_grpc_server
from contextlib import asynccontextmanager

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):

    threading.Thread(
        target=start_grpc_server,
        daemon=True
    ).start()

    print("gRPC thread started")

    yield

    print("Application shutdown")

app = FastAPI(
    title="Like Service API",
    description="API for managing likes on posts",
    lifespan=lifespan,
)
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
    return {"status": "ok", "service": "like-service"}


@app.get("/likes")
def get_likes(db: Session = Depends(get_db)):
    return db.query(Like).all()



@app.post("/likes")
def create_like(post_id: int, db: Session = Depends(get_db)):
    new_like = Like(post_id=post_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return new_like


@app.get("/posts/{post_id}/likes_count")
def get_likes_count(post_id: int, db: Session = Depends(get_db)):
    count= db.query(Like).filter(Like.post_id == post_id).count()
    return {"post_id": post_id, "likes_count": count}

@app.delete("/likes/{like_id}")
def delete_like(like_id: int, db: Session = Depends(get_db)):
    like = db.query(Like).filter(Like.id == like_id).first()
    if like:
        db.delete(like)
        db.commit()
        return {"message": f"Like with id {like_id} deleted"}
    else:
        raise HTTPException(status_code=404, detail={"message": f"Like with id {like_id} not found"})
    
@app.get("/likes/{like_id}")
def get_like(like_id: int, db: Session = Depends(get_db)):
    like = db.query(Like).filter(Like.id == like_id).first()
    if like:
        return like
    else:
        raise HTTPException(status_code=404, detail={"message": f"Like with id {like_id} not found"})
