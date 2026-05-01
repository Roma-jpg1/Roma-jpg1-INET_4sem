from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Booking(BaseModel):
    id: int
    date: str

class CreateBooking(BaseModel):
    date: str

bookings_db: List[Booking] = [
    Booking(id=1, date="2023-10-01"),
    Booking(id=2, date="2023-10-02"),
]

next_id = len(bookings_db) + 1

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/bookings", response_model=List[Booking])
def get_bookings():
    return bookings_db

@app.post("/bookings", response_model=Booking)
def create_booking(booking: CreateBooking):
    global next_id
    new_booking = Booking(id=next_id, date=booking.date)
    bookings_db.append(new_booking)
    next_id += 1
    return new_booking

@app.get("/bookings/{booking_id}", response_model=Booking)
def get_booking(booking_id: int):
    for b in bookings_db:
        if b.id == booking_id:
            return b
    raise HTTPException(status_code=404, detail="Booking not found")