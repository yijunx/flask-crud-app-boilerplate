import casbin_sqlalchemy_adapter
import casbin
from pydantic.utils import path_type
from app.config.app_config import conf
from app.casbin.role_definition import (
    SpecificResourceRightsEnum,
    resource_right_action_mapping,
    ResourceActionsEnum,
)
import app.repo.casbin_rule as casbinruleRepo
from app.db.database import SessionLocal
from contextlib import contextmanager
from app.schemas.casbin_rule import CasbinPolicy

from app.schemas.user import User
from datetime import datetime, timezone


RESOURCE = "/items"


@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        # can roll other things back here
        raise
    finally:
        session.close()


def create_casbin_enforcer():
    adapter = casbin_sqlalchemy_adapter.Adapter(conf.DATABASE_URI)
    casbin_enforcer = casbin.Enforcer("app/casbin/model.conf", adapter)
    # probably need to come from configurations?
    # now added a function here to
    print("creating casbin enforcer")

    def actions_mapping(action: str, resource_right: str) -> bool:
        """
        actions are get download patch share...
        resource_right are own / edit / view
        """
        if resource_right in resource_right_action_mapping:
            if action in resource_right_action_mapping[resource_right]:
                return True
        return False

    casbin_enforcer.add_function("actions_mapping", actions_mapping)
    # add admin role, only admin can create
    # well we cannot add policy this way because there are additional columns
    # casbin_enforcer.add_policy("admin-user-id", RESOURCE, ResourceActionsEnum.create.name)
    # casbin_enforcer.add_grouping_policy("admin-user-id", "admin-role-id")

    return casbin_enforcer


casbin_enforcer = create_casbin_enforcer()


def is_admin(user: User):
    with get_db() as db:
        is_admin = any(
            x
            for x in casbinruleRepo.get_role_ids_of_user(db=db, user_id=user.id)
            if x.v1 == conf.ADMIN_ROLE_ID
        )
    return is_admin


def construct_role_name(item_id: str) -> str:
    pass


def create_roles_for_resource(item_id: str):
    return


def bind_user_to_resource(user_id: str, item_id: str, role: str):
    return


def get_permissions_for_user(user_id: str, action: str):
    return


def has_admin_access(user_id) -> bool:
    return


def create_admin_access(user_id):
    # run when flask starting
    # this is to make sure the first admin exists..
    # check how the seed works
    return
