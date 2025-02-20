from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


#Auto generated Documentation
#127.0.0.1:8000/docs#


app = FastAPI()

class Item(BaseModel):
    text: str
    is_done: bool = False


items = []


@app.get("/")
def root():
    return {"Hello":"World"}


@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items


@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]


@app.get("/items")
def get_all_items():
    return items


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id:int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")