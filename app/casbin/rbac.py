from casbin import enforcer
import casbin_sqlalchemy_adapter
import casbin
from app.config.app_config import conf
from role_definition import resource_right_action_mapping, ResourceActionsEnum


adapter = casbin_sqlalchemy_adapter.Adapter(conf.DATABASE_URI)
casbin_enforcer = casbin.Enforcer("app/casbin/model.conf", adapter)


# probably need to come from configurations?
# now added a function here to 
RESOURCE = "/items"
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
casbin_enforcer.add_policy("admin_role_id", RESOURCE, ResourceActionsEnum.create.name)
# add this user to admin 
casbin_enforcer.add_grouping_policy("admin_user_id", "admin_role_id")


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




