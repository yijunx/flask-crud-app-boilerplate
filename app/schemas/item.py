from pydantic import BaseModel
from app.schemas.pagination import ResponsePagination
from datetime import datetime
from typing import List, Optional
from app.casbin.role_definition import SpecificResourceRightsEnum


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


class ItemWithPaging(BaseModel):
    data: List[Item]
    paging: ResponsePagination


class UsersItemRight(BaseModel):
    """resource_id's relation to a specific user"""

    user_id: str
    right: Optional[SpecificResourceRightsEnum]  # own / edit / view


class UsersItemRightWithPaging(BaseModel):
    data: List[UsersItemRight]
    paging: ResponsePagination
