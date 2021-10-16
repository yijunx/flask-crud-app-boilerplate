from flask import Blueprint
from app.util.response_util import create_response
from app.util.app_logging import get_logger


bp = Blueprint("internal", __name__, url_prefix="/internal")
logger = get_logger(__name__)


@bp.route("/liveness", methods=["GET"])
def liveness_probe():
    return {"am i ok": "yes"}
