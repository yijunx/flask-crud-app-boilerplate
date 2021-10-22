from flask import Blueprint
from app.util.response_util import create_response
from app.util.app_logging import get_logger


bp = Blueprint("rbac", __name__, url_prefix="/internal/rbac")
logger = get_logger(__name__)


@bp.route("/info", methods=["GET"])
def rbac_info():
    return {"well this is": "rbac info"}


@bp.route("/admin_users", methods=["GET"])
def list_admin_users():
    # need to check if this is comming from a user admin..
    return "not yet"


@bp.route("/admin_users", methods=["POST"])
def add_admin_user():
    # need to check if this is comming from a user admin..
    return "not yet"


@bp.route("/admin_users/<user_id>", methods=["DELETE"])
def delete_admin_user():
    # need to check if this is comming from a user admin..
    return "not yet"
