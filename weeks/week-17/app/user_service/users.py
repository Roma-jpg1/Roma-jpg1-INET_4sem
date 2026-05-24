from unittest.mock import Base
from .db import SessionLocal, engine, Base
from .models import User
from fastapi import Depends, FastAPI, HTTPException
from pytest import Session
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service API", description="API for managing users")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/users")
def create_user(email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = password + "_hashed"

    if exisits := db.query(User).filter(User.email == email).first():
        return {"message": f"User with email {email} already exists"}
    
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": f"User with id {user_id} deleted"}
    else:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")