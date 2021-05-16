import uvicorn
from typing import Optional, List
from enum import Enum
from fastapi import FastAPI, Query
from pydantic import BaseModel


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
    nae: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None





@app.get('/items/', tags=['Declare more metadata'])
async def read_items(
    q: Optional[str] = Query(
        None, 
        title="ajdkfjas;dfjaksldfjklasdjfklsdjflkasjdfklasj;dfkljasd;lkfjsdklfjakl;sd", 
        description="Query string for the items to search in the database that have a good match",
        min_length=3
        )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q":q})
    return results


@app.get('/item/', tags=['Alias parameters¶'])
async def read_items(
    q: Optional[str] = Query(
        None, 
        alias="item-query",
        min_length=3
        )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q":q})
    return results




if __name__  == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)