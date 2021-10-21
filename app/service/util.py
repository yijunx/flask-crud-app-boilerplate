RESOURCE_NAME = "items/"


def get_resource_id(item_id: str) -> str:
    return f"{RESOURCE_NAME}{item_id}"


def get_item_id(resource_id: str) -> str:
    if resource_id.startswith(RESOURCE_NAME):
        return resource_id[len(RESOURCE_NAME) :]
    else:
        raise Exception("resource id not starting with resource name..")
