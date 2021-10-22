from functools import wraps, partial
from app.casbin.rbac import create_casbin_enforcer
from app.exceptions.rbac import NotAuthorized
from app.schemas.user import User
from app.casbin.role_definition import SpecificResourceActionsEnum

RESOURCE_NAME = "items/"
casbin_enforcer = create_casbin_enforcer()


def get_resource_id(item_id: str) -> str:
    return f"{RESOURCE_NAME}{item_id}"


def get_item_id(resource_id: str) -> str:
    if resource_id.startswith(RESOURCE_NAME):
        return resource_id[len(RESOURCE_NAME) :]
    else:
        raise Exception("resource id not starting with resource name..")


def authorize(action: SpecificResourceActionsEnum, admin_required: bool = False):
    """
    Enforces authorization on all service layer with item_id and user.
    The function name must have the pattern <act>_item
    """

    @wraps
    def decorator(func):
        @wraps
        def wrapper_enforcer(*args, **kwargs):
            item_id: str = kwargs["item_id"]
            user: User = kwargs["user"]
            if user.is_admin:  # admin.. so let him go..
                return func(*args, **kwargs)
            # now user is not admin
            if admin_required:
                raise NotAuthorized(
                    resource_id=item_id, operation=action, user_id=user.id
                )
            # now this is not admin only stuff, start the normal casbin
            if casbin_enforcer.enforce(user.id, item_id, action):
                return func(*args, **kwargs)
            else:
                raise NotAuthorized(
                    resource_id=item_id, operation=action, user_id=user.id
                )

        return wrapper_enforcer

    return decorator
