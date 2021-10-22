from enum import Enum


class PolicyTypeEnum(str, Enum):
    """p for policy, g for grouping"""

    p = "p"
    g = "g"


class SpecificResourceRightsEnum(str, Enum):
    """one user of one resource can only be one of the below"""

    view = "view"  # user is viewer
    edit = "edit"  # user is editor
    own = "own"  # user is owner


class ResourceActionsEnum(str, Enum):
    """actions to happen on resource/ without id"""

    get_all = "get_all"
    create = "create"


class SpecificResourceActionsEnum(str, Enum):
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
        SpecificResourceActionsEnum.get,
        SpecificResourceActionsEnum.download,
    },
    SpecificResourceRightsEnum.edit: {
        SpecificResourceActionsEnum.get,
        SpecificResourceActionsEnum.download,
        SpecificResourceActionsEnum.patch,
    },
    SpecificResourceRightsEnum.own: {
        SpecificResourceActionsEnum.get,
        SpecificResourceActionsEnum.download,
        SpecificResourceActionsEnum.patch,
        SpecificResourceActionsEnum.share,
        SpecificResourceActionsEnum.unshare,
        SpecificResourceActionsEnum.delete,
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
