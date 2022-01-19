from typing import Optional

from fastapi import FastAPI
import consumer

app = FastAPI()


@app.get("/")
def read_root():
    consumer.callback()
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}