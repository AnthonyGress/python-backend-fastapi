from pydantic import BaseModel
from enum import Enum

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"

class Item(BaseModel):
    name: str | None = None
    price: float | None = None
    count: int | None = None
    id: int | None = None
    category: Category | None = None
