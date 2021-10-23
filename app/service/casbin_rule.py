from datetime import datetime, timezone
from app.db.database import get_db
from app.exceptions.rbac import NotAuthorized
from app.schemas.item import Item, ItemCreate, ItemWithPaging, ItemPatch, ItemsUserRight
from app.schemas.pagination import QueryPagination
from app.schemas.user import User, UserShare, UsersItemRight
from app.schemas.casbin_rule import CasbinPolicy
import app.repo.item as itemRepo
import app.repo.casbin_rule as casbinruleRepo
from app.casbin.rbac import create_casbin_enforcer
from app.casbin.role_definition import (
    SpecificResourceRightsEnum,
    SpecificResourceActionsEnum,
    PolicyTypeEnum,
)
from app.service.util import get_resource_id, get_item_id, authorize
from app.config.app_config import conf


casbin_enforcer = create_casbin_enforcer()



