import uvicorn
from typing import Optional
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




@app.post("/items/")
async def create_item(item:Item):
    return item


# Required query parameters
@app.get("/items/{items_id}")
async def read_user_item(
    item_id: int, needy: str, skip: int = 0, limit: Optional[int] = None
):
    item = {"item_id": item_id, "needy": needy}
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short:bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )

    return item



@app.get("/items/{item_id}")
async def read_item(item_id:str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q: 
        item.update({"q":q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10, category: str = ""):
    return fake_items_db[skip: skip+limit]


@app.get('/files/{file_path:path}')
async def read_file(file_path:str):
    return {"file_path": file_path}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "have some residuals"}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/items/{item_id}")
async def root(item_id: int):
    return {"item_id": item_id}

# Query Parameters and String Validations
@app.get('/items/')
async def read_items(q: Optional[str] = Query(None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q":q})
    return results

# Add more validations
@app.get('/items/')
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q":q})
    return results

if __name__  == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)