from flask import Blueprint, request
from flask_pydantic import validate
from app.schemas.item import ItemCreate
from app.schemas.pagination import QueryPagination
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
    _ = get_user_info_from_request(request=request)
    r = itemService.list_items(query_pagination=query)
    return create_response(response=r)


@bp.route("", methods=["POST"])
@validate()
def post_item(body: ItemCreate):
    user = get_user_info_from_request(request=request)
    try:
        r = itemService.create_item(item_create=body, user=user)
    except (ItemNameIsAlreadyThere, ) as e:
        return create_response(status_code=e.status_code, message=e.message, success=False)
    except Exception as e:
        logger.error(e, exc_info=True)
        return create_response(status_code=500, message=str(e), success=False)
    return create_response(response=r)


@bp.route("/<item_id>", methods=["GET"])
def get_item(item_id: str):
    _ = get_user_info_from_request(request=request)
    # check casbin here...
    try:
        r = itemService.get_item(item_id=item_id)
    except (ItemDoesNotExist,) as e:
        return create_response(
            success=False, message=e.message, status_code=e.status_code
        )
    return create_response(response=r)


@bp.route("/<item_id>", methods=["DELETE"])
def delete_item(item_id: str):
    _ = get_user_info_from_request(request=request)
    # check casbin here...
    _ = itemService.delete_item(item_id=item_id)
    return create_response(message="item deleted")
