from flask import Flask, Response
from flask.helpers import make_response
from flask_request_id_header.middleware import RequestID
from flask_cors import CORS
from app.util.app_logging import get_logger, init_logger
from app.blueprints.item import bp as itemBp
from app.blueprints.interntal import bp as internalBp
from app.util.response_util import create_response
from app.config.app_config import conf


logger = get_logger(__name__)

app = Flask(__name__)
init_logger(app=app)
# app.json_encoder = some custom json encoder... (to deal with some datetime issues)
app.config["REQUEST_ID_UNIQUE_VALUE_PREFIX"] = ""
CORS(app, resources={r"/api/*": {"origins": conf.CORS_ALLOWED_ORIGINS}})


# blue prints
app.register_blueprint(itemBp)
app.register_blueprint(internalBp)


@app.after_request
def modify_flask_pydantic_response(response: Response):
    if (
        response.status_code == 400
        and response.is_json
        and "validation_error" in response.json
    ):
        logger.info(response.json)
        message = "The problem is in the validation"
        return create_response(message=message, status_code=400)
    return response


@app.errorhandler(500)
def unhandled_internal_server_error(err):
    logger.error(err, exc_info=True)
    return create_response(message=err, status_code=500, success=False)
