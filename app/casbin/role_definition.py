from enum import Enum, auto
from pydantic import BaseModel


class SpecificResourceRightsEnum(Enum):
    """one user can only be one of the below"""
    view = "view"  # user is viewer
    edit = "edit"  # user is editor
    own = "own"   # user is owner


class ResourceActionsEnum(Enum):
    """actions to happen on resource/ without id"""
    get_all = "get_all"
    create = "create"


class SpecificResourceActionsEnum(Enum):
    """these are the actions to happen on a resource/resource_id"""
    get = "get"
    download = "download"
    patch = "patch"
    share = "share"
    unshare = "unshare"
    delete = "delete"
    

# this is dynamic
resource_right_action_mapping: dict = {
        SpecificResourceRightsEnum.view: {
            SpecificResourceActionsEnum.get.name,
            SpecificResourceActionsEnum.download.name
        },
        SpecificResourceRightsEnum.edit.name: {
            SpecificResourceActionsEnum.get.name,
            SpecificResourceActionsEnum.download.name,
            SpecificResourceActionsEnum.patch.name
        },
        SpecificResourceRightsEnum.own.name: {
            SpecificResourceActionsEnum.get.name,
            SpecificResourceActionsEnum.download.name,
            SpecificResourceActionsEnum.patch.name,
            SpecificResourceActionsEnum.share.name,
            SpecificResourceActionsEnum.unshare.name,
            SpecificResourceActionsEnum.delete.name
        },
    }





# class ViewActionsEnum(Enum):
#     get = "get"


# class EditActionsEnum(Enum):
#     patch = "patch"


# class OwnActionsEnum(Enum):
#     delete = "delete"
#     share = "share"
#     unshare = "unshare"


