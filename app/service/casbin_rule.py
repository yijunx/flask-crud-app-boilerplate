from datetime import datetime, timezone

from pydantic.utils import path_type
from app.db.database import get_db
from app.exceptions.rbac import NotAuthorized
from app.schemas.item import Item, ItemCreate, ItemWithPaging, ItemPatch, ItemsUserRight
from app.schemas.pagination import QueryPagination
from app.schemas.user import User, UserShare, UsersItemRight
from app.schemas.casbin_rule import CasbinPolicy
import app.repo.item as itemRepo
import app.repo.casbin_rule as casbinruleRepo
from app.casbin.role_definition import (
    SpecificResourceRightsEnum,
    SpecificResourceActionsEnum,
    PolicyTypeEnum,
)
from app.service.util import get_resource_id, get_item_id, authorize
from app.config.app_config import conf


# this is internal, receiving instructions from user management!
# user management will add auth to check
# whether a user can use the service to call the internal endpoint here
def add_admin(admin_user_id: str, user: User):
    with get_db() as db:
        group_policy = CasbinPolicy(
            ptype=PolicyTypeEnum.g, v0=admin_user_id, v1=conf.ADMIN_ROLE_ID
        )
        casbinruleRepo.create(db=db, casbin_policy=group_policy)


def delete(admin_user_id: str, user: User):
    with get_db() as db:
        group_policy = CasbinPolicy(
            ptype=PolicyTypeEnum.g, v0=admin_user_id, v1=conf.ADMIN_ROLE_ID
        )
        casbinruleRepo.create(db=db, casbin_policy=group_policy)


def list_admin(admin_user_id: str, user: User) -> bool:
    with get_db() as db:
        group_policy = CasbinPolicy(
            ptype=PolicyTypeEnum.g, v0=admin_user_id, v1=conf.ADMIN_ROLE_ID
        )
        casbinruleRepo.create(db=db, casbin_policy=group_policy)


def is_admin(user: User):
    with get_db() as db:
        is_admin = any(
            x
            for x in casbinruleRepo.get_role_ids_of_user(db=db, user_id=user.id)
            if x.v1 == conf.ADMIN_ROLE_ID
        )
    return is_admin
