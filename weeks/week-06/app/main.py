from typing import List, Dict, Optional
from fastapi import FastAPI
from pydantic import BaseModel
import strawberry
from strawberry.fastapi import GraphQLRouter

app = FastAPI()


@strawberry.type
class Book:
    name: str
    serial: str
    id : int 


book_db: List[Book] = [
    Book(name="lobzik",serial="S1", id=1),
    Book(name="screbok",serial="S2", id=2),
]

next_id = len(book_db)+1


@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> List[Book]:
        return book_db

    @strawberry.field
    def book(self, id: int) -> Optional[Book]:
        for book in book_db:
            if book.id == id:
                return book
        return None
    
@strawberry.type
class Mutation:
    @strawberry.mutation
    def createBook(self, name: str, serial: str) -> Book:
        global next_id

        new_book = Book(
            id=next_id,
            name=name,
            serial=serial
        )
        book_db.append(new_book)
        next_id += 1
        return new_book

@app.get("/book", response_model=List[Book])
def get_a():
    return book_db


graphql_app = GraphQLRouter(strawberry.Schema(query=Query, mutation=Mutation))
app.include_router(graphql_app, prefix="/graphql")



