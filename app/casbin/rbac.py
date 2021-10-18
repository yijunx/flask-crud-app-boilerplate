import casbin_sqlalchemy_adapter
import casbin
from app.config.app_config import conf
from role_definition import RolesEnum


adapter = casbin_sqlalchemy_adapter.Adapter(conf.DATABASE_URI)
casbin_enforcer = casbin.Enforcer("app/casbin/model.conf", adapter)


# probably need to come from configurations?





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




