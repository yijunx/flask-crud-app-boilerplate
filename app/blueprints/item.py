from flask import Blueprint, request
from flask_pydantic import validate
from app.exceptions.casbin_rule import PolicyDoesNotExist, PolicyIsAlreadyThere
from app.exceptions.rbac import NotAuthorized
from app.schemas.item import ItemCreate, ItemPatch
from app.schemas.pagination import QueryPagination
from app.schemas.user import UserShare
from app.util.response_util import create_response
import app.service.item as itemService
from app.util.app_logging import get_logger
from app.util.process_request import get_user_info_from_request
from app.exceptions.item import ItemDoesNotExist, ItemNameIsAlreadyThere


bp = Blueprint("item", __name__, url_prefix="/api/items")
logger = get_logger(__name__)


@bp.route("", methods=["GET"])
@validate()
def list_items(query: QueryPagination):
    user = get_user_info_from_request(request=request)
    r = itemService.list_items(query_pagination=query, user=user)
    return create_response(response=r)


@bp.route("", methods=["POST"])
@validate()
def post_item(body: ItemCreate):
    user = get_user_info_from_request(request=request)
    try:
        r = itemService.create_item(item_create=body, user=user)
    except (ItemNameIsAlreadyThere,) as e:
        return create_response(
            status_code=e.status_code, message=e.message, success=False
        )
    except Exception as e:
        return create_response(status_code=500, message=str(e), success=False)
    return create_response(response=r)


@bp.route("/<item_id>", methods=["GET"])
def get_item(item_id: str):
    user = get_user_info_from_request(request=request)
    # check casbin here...
    try:
        r = itemService.get_item(item_id=item_id, user=user)
    except (ItemDoesNotExist, NotAuthorized) as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=r)


@bp.route("/<item_id>", methods=["PATCH"])
@validate()
def patch_item(item_id: str, body: ItemPatch):
    user = get_user_info_from_request(request=request)
    # check casbin here...
    try:
        r = itemService.patch_item(item_id=item_id, user=user, item_patch=body)
    except (ItemDoesNotExist, NotAuthorized) as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(response=r)


@bp.route("/<item_id>", methods=["DELETE"])
def delete_item(item_id: str):
    user = get_user_info_from_request(request=request)
    # check casbin here...
    # always need to pass the user because need to ask casbin for auth
    try:
        itemService.delete_item(item_id=item_id, user=user)
    except (ItemDoesNotExist, NotAuthorized) as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.debug(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(message="item deleted")


@bp.route("/<item_id>/sharees", methods=["POST"])
@validate()
def share_item(item_id: str, body: UserShare):
    user = get_user_info_from_request(request=request)
    try:
        itemService.share_item(item_id=item_id, user=user, user_share=body)
    except (ItemDoesNotExist, NotAuthorized, PolicyIsAlreadyThere) as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(message="item shared")


@bp.route("/<item_id>/sharees", methods=["GET"])
def list_shares(item_id: str):
    user = get_user_info_from_request(request=request)

    pass


@bp.route("/<item_id>/sharees/<sharee_id>", methods=["DELETE"])
def unshare_item(item_id: str, sharee_id: str):
    user = get_user_info_from_request(request=request)
    try:
        itemService.unshare_item(item_id=item_id, user=user, sharee_id=sharee_id)
    except (ItemDoesNotExist, NotAuthorized, PolicyDoesNotExist) as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        return create_response(success=False, message=str(e), status_code=500)
    return create_response(message="sharee deleted")


@bp.route("/<item_id>/sharees/<sharee_id>", methods=["PATCH"])
def update_item_sharing_info(item_id: str, sharee_id: str):
    user = get_user_info_from_request(request=request)
    # check casbin here...
    # always need to pass the user because need to ask casbin for auth
    _ = itemService.delete_item(item_id=item_id, user=user)
    return create_response(message="sharee updated")
