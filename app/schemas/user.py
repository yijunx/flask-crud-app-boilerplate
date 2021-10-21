from pydantic import BaseModel
from app.casbin.role_definition import SpecificResourceRightsEnum
from typing import Optional, List

from app.schemas.pagination import ResponsePagination


class User(BaseModel):
    id: str
    name: str  # maybe only first name from google id token
    email: str
    is_admin: bool = False


class UsersItemRight(BaseModel):
    """used for select all policies for a given user"""

    user_id: str
    right: Optional[SpecificResourceRightsEnum]  # own / edit / view


class UsersItemRightWithPaging(BaseModel):
    data: List[UsersItemRight]
    paging: ResponsePagination


class UserShare(BaseModel):
    """the schema for the payload to share/unshare a user"""

    user_id: str
    right: SpecificResourceRightsEnum
