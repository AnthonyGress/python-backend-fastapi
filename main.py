from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from models import Item
from data import items

app = FastAPI()

@app.get("/")
def index () -> dict[str, dict[int, Item]]:
    return {"items": items}

@app.get("/items/{item_id}")
def get_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail=f"Item with {item_id=} does not exist"
        )
    return items[item_id]

@app.post("/items")
def add_item(item: Item) -> dict[str, Item]:
    if item.id in items:
        HTTPException(status_code=400, detail=f"Item with {item.id=} already exists")
    items[item.id] = item
    return {"added": item}

@app.put("/items/{item_id}")
def update (
    item_id: int,
    item: Item
) -> dict[str, Item]:

    update_item_encoded = jsonable_encoder(item)

    if item_id not in items:
        HTTPException(status_code=400, detail=f"Item with {item_id=} does not exist")
    if all(info is None for info in (item.name, item.price, item.count)):
        raise HTTPException(
            status_code=400, detail="No parameters provided for update."
    )
    item = items[item_id]
    if update_item_encoded["name"]is not None:
        item.name = update_item_encoded["name"]
    if update_item_encoded["price"] is not None:
        item.price = update_item_encoded["price"]
    if update_item_encoded["price"] is not None:
        item.count = update_item_encoded["price"]

    return {"updated": update_item_encoded}

@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        HTTPException(status_code=400, detail=f"Item with {item_id=} does not exist")

    item = items.pop(item_id)
    return {"deleted": item}
