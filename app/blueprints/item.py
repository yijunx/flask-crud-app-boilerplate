from flask import Blueprint, request
from flask_pydantic import validate
from app.schemas.item import ItemCreate
from app.schemas.pagination import QueryPagination
from app.util.response_util import create_response
import app.service.item as itemService
from app.util.app_logging import get_logger
from app.util.process_request import get_user_info_from_request
from app.exceptions.item import ItemDoesNotExist


bp = Blueprint("internal", __name__, url_prefix="/api/items")
logger = get_logger(__name__)


@bp.route("", methods=["GET"])
def list_items(query: QueryPagination):
    _ = get_user_info_from_request(request=request)
    r = itemService.list_items(query_pagination=query)
    return create_response(response=r)


@bp.route("", methods=["POST"])
def post_item(body: ItemCreate):
    user = get_user_info_from_request(request=request)
    r = itemService.create_item(item_create=body, user=user)
    return create_response(response=r)


@bp.route("/<item_id>", methods=["GET"])
def delete_item(item_id: str):
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
    r = itemService.delete_item(item_id=item_id)
    return create_response(response=r)
