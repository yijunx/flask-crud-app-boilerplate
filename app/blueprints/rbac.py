from flask import Blueprint, request
from app.util.process_request import get_user_info_from_request
from app.util.response_util import create_response
from app.util.app_logging import get_logger
import app.service.casbin_rule as casbinruleService


bp = Blueprint("rbac", __name__, url_prefix="/internal/rbac")
logger = get_logger(__name__)


@bp.route("/info", methods=["GET"])
def rbac_info():
    return {"well this is": "rbac info"}


@bp.route("/admin_users", methods=["GET"])
def list_admin_users():
    # need to check if this is comming from a user admin..
    return "not yet"


@bp.route("/admin_user/<user_id>", methods=["GET"])
def check_if_its_admin_user(user_id: str):
    # return 404 if not..
    user = get_user_info_from_request(request=request)
    if user.is_admin:
        return create_response(status_code=200)
    else:
        return create_response(status_code=404)


@bp.route("/admin_users", methods=["POST"])
def add_admin_user():
    # need to check if this is comming from a user admin..
    return "not yet"


@bp.route("/admin_users/<user_id>", methods=["DELETE"])
def delete_admin_user():
    # need to check if this is comming from a user admin..
    return "not yet"
