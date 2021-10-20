from pydantic import BaseModel
from app.casbin.role_definition import SpecificResourceRightsEnum
from typing import Optional, List

from app.schemas.pagination import ResponsePagination


class User(BaseModel):
    id: str
    name: str  # maybe only first name from google id token
    email: str


class UsersItemRight(BaseModel):
    """resource_id's relation to a specific user"""

    user_id: str
    right: Optional[SpecificResourceRightsEnum]  # own / edit / view


class UsersItemRightWithPaging(BaseModel):
    data: List[UsersItemRight]
    paging: ResponsePagination
