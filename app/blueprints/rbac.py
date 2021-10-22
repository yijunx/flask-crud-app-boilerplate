from flask import Blueprint
from app.util.response_util import create_response
from app.util.app_logging import get_logger


bp = Blueprint("internal", __name__, url_prefix="/internal/rbac")
logger = get_logger(__name__)


@bp.route("/info", methods=["GET"])
def rbac_info():
    return {"well this is": "rbac info"}
