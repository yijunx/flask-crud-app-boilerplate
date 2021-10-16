from pydantic import BaseModel
from app.schemas.pagination import ResponsePagination
from datetime import datetime
from typing import List


class ItemCreate(BaseModel):
    name: str
    description: str


class ItemPatch(BaseModel):
    description: str


class Item(ItemCreate):
    id: str
    created_at: datetime
    created_by: str
    created_by_name: str

    class Config:
        orm_mode = True


class ItemWithPagination(BaseModel):
    data: List[Item]
    paging: ResponsePagination
