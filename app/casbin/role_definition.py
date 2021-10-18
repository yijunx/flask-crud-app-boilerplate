from enum import Enum


class RolesEnum(Enum):
    """one user can only be one of the below"""
    viewer = "view"
    editor = "edit"
    owner = "own"


# class ViewActionsEnum(Enum):
#     get = "get"


# class EditActionsEnum(Enum):
#     patch = "patch"


# class OwnActionsEnum(Enum):
#     delete = "delete"
#     share = "share"
#     unshare = "unshare"


