from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/other")
def get():
    return {"mess":"pwgegjkgkdjlsjlkdsskjl ds"}