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
    admin_right = "admin_right"


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

    lock = "lock"  # lock item from being edited
    ban = "ban"    # ban user from this service
    unban = "unban" # unban


# this is dynamic
# this is make sure that, own covers edit, edit covers view
# this also supports other relations, very customization
resource_right_action_mapping: dict = {
    SpecificResourceRightsEnum.view: {
        SpecificResourceActionsEnum.get,
        SpecificResourceActionsEnum.download,
    },
    SpecificResourceRightsEnum.edit: {
        SpecificResourceActionsEnum.get,
        SpecificResourceActionsEnum.download,
        # edit only
        SpecificResourceActionsEnum.patch,
    },
    SpecificResourceRightsEnum.own: {
        SpecificResourceActionsEnum.get,
        SpecificResourceActionsEnum.download,
        SpecificResourceActionsEnum.patch,
        # own only
        SpecificResourceActionsEnum.share,
        SpecificResourceActionsEnum.unshare,
        SpecificResourceActionsEnum.delete,
    },
    SpecificResourceRightsEnum.admin_right: {
        SpecificResourceActionsEnum.get,
        SpecificResourceActionsEnum.download,
        SpecificResourceActionsEnum.patch,
        SpecificResourceActionsEnum.share,
        SpecificResourceActionsEnum.unshare,
        SpecificResourceActionsEnum.delete,
        # admin only
        SpecificResourceActionsEnum.lock,
        SpecificResourceActionsEnum.ban,
        SpecificResourceActionsEnum.unban
    }
}
