import uvicorn
from typing import Optional, List
from enum import Enum
from fastapi import FastAPI, Query, Path , Body
from pydantic import BaseModel, Field


class ModelName(str, Enum):
    resnet = "resnet"
    lenet = "lenet"

fake_items_db = [
    {"item_name":"Foo"},
    {"item_name":"Bar"},
    {"item_name":"Baz"},
    ]

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="the description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="the price must be greater than zero")
    tax: Optional[float] = None

class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, 'item': item}
    return results

@app.put("/Singular values in body/{item_id}")
async def update_item(
    *,
    item_id: int ,
    item: Item,
    user: User,
    importance: int = Body(..., gt=0),
):
    results = {
        "item_id" : item_id,
        "item" : item,
        "user" : user,
        "importance": importance,
    }
    return results

@app.put("/Embed a single body parameter/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=False)):
    results = {"item_id": item_id, "item": item}
    return results


if __name__  == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)