from functools import wraps, partial
from app.casbin.rbac import create_casbin_enforcer
from app.exceptions.rbac import NotAuthorized
from app.schemas.user import User
from app.casbin.role_definition import SpecificResourceActionsEnum
from app.config.app_config import conf

casbin_enforcer = create_casbin_enforcer()


def get_resource_id(item_id: str) -> str:
    return f"{conf.RESOURCE_NAME}{item_id}"


def get_item_id(resource_id: str) -> str:
    if resource_id.startswith(conf.RESOURCE_NAME):
        return resource_id[len(conf.RESOURCE_NAME) :]
    else:
        raise Exception("resource id not starting with resource name..")


def authorize(action: SpecificResourceActionsEnum, admin_required: bool = False):
    """
    Enforces authorization on all service layer with item_id and user.
    The function name must have the pattern <act>_item

    This decorator is not used on flask endpoints because it can be decoupled with
    the request path. (it does not nessisarily needs to take user/item id from request)
    """

    def decorator(func):
        def wrapper_enforcer(*args, **kwargs):
            item_id: str = kwargs["item_id"]
            resource_id: str = get_resource_id(item_id)
            user: User = kwargs["user"]
            if user.is_admin:  # admin.. so let him go..
                print("casbin allows it because he/she is admin!")
                return func(*args, **kwargs)
            # now user is not admin
            if admin_required:
                raise NotAuthorized(
                    resource_id=resource_id, action=action, user_id=user.id
                )
            # now this is not admin only stuff, start the normal casbin
            if casbin_enforcer.enforce(user.id, resource_id, action):
                print("casbin allows it..!")
                return func(*args, **kwargs)
            else:
                raise NotAuthorized(
                    resource_id=item_id, action=action, user_id=user.id
                )

        return wrapper_enforcer

    return decorator
