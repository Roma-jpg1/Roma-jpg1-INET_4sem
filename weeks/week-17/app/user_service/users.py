from db import SessionLocal, engine, Base
from models import User
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text


Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service API", description="API for managing users")

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
    return {"status": "ok", "service": "user-service"}


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/users")
def create_user(email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = password + "_hashed"

    if existing_user := db.query(User).filter(User.email == email).first():
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
