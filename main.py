import uvicorn
from typing import Optional, List
from enum import Enum
from fastapi import FastAPI, Query, Path
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


@app.get('/Deprecating parameters/', tags=['Deprecating parameters'])
async def read_items(
    q: Optional[str] = Query(
        None, 
        alias="아이템 쿼리",
        title="쿼리 문자",
        description="설명문서에요.",
        min_length=3,
        max_length=10,
        regex="^한글로입력$",
        deprecated=True
        )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q":q})
    return results

@app.get("/Declare metadata/{item_id}", tags=['Declare metadata'])
async def read_items(
    item_id: int = Path(..., title='The ID of the item to get'),
    q: Optional[str] = Query(None, alias='item-query'),
):
    results = {'item_id': item_id}
    if q:
        results.update({'q':q})
    return results

@app.get("/Order the parameters as you need/{item_id}", tags=['Order the parameters as you need'])
async def read_items(
    q: str,
    item_id: int = Path(..., title='The ID of the item to get'),
):
    results = {'item_id': item_id}
    if q:
        results.update({'q':q})
    return results

@app.get("/Order the parameters as you need, tricks/{item_id}")
async def read_items(
    *, item_id: int = Path(..., title="The ID of the item to get"), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get('/Number validations: greater than or equal/{item_id}')
async def read_items(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=1),
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({'q':q})
    return results


@app.get('/Number validations: greater than and less than or equal/{item_id}')
async def read_items(
    *,
    item_id: int = Path(..., title="The ID of the item to get", gt=0, le=100),
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({'q':q})
    return results

@app.get('/Number validations: floats, greater than and less than/{item_id}')
async def read_items(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=100),
    q: str,
    size: float = Query(..., gt=0, lt=10.5)
):
    results = {"item_id": item_id}
    if q:
        results.update({'q':q})
    return results




if __name__  == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)